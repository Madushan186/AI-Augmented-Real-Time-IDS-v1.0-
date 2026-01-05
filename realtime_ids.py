import os
import json
import time
import joblib
import numpy as np
import pandas as pd
from scapy.all import sniff, TCP, UDP, ICMP, IP
from collections import deque
import datetime
import sys



# --- CONFIGURATION ---
MODEL_PATH = "models/rf_ids_model.pkl"
STATE_FILE = "ids_state.json"
LOG_FILE = "attack_log.csv"

# ULTRATHINK OPTIMIZATION SETTINGS
# Window: 1.0 second (Instant Feedback). 
# Threshold: 10 requests. (Anything > 10 req/s is flagged)
HTTP_WINDOW_SECONDS = 0.5
HTTP_REQ_THRESHOLD = 40

COOLDOWN_DURATION = 0.1    # 0.1s for INSTANT recovery after attack stops

# --- GLOBAL STATE ---
# Sliding Window for Rate Calculation
packet_times = deque(maxlen=2000)
http_requests = deque(maxlen=2000)

# State management variables
current_status = "Normal"
last_attack_time = 0.0
total_packets = 0
total_attacks = 0

# Load trained Machine Learning Model
try:
    model = joblib.load(MODEL_PATH)
    print(f"✅ [INIT] Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"⚠️ [INIT] Error loading model: {e}")
    model = None

start_time = time.time()

# 41 Features used in CICIDS2017 Dataset
columns = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes",
    "land","wrong_fragment","urgent","hot","num_failed_logins","logged_in",
    "num_compromised","root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files","num_outbound_cmds",
    "is_host_login","is_guest_login","count","srv_count","serror_rate",
    "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate","dst_host_count",
    "dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate","dst_host_srv_diff_host_rate",
    "dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate"
]

def log_attack(attack_type, rate):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write("timestamp,attack_type,rate\n")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp},{attack_type},{rate:.2f}\n")

def update_state_file(status, total, attacks, **kwargs):
    state = {
        "total": total,
        "attacks": attacks,
        "status": status,
        "last_features": kwargs.get("last_features", "Waiting for traffic..."),
        "model_status": kwargs.get("model_status", "Unknown")
    }
    tmp_file = f"{STATE_FILE}.tmp"
    try:
        with open(tmp_file, "w") as f:
            json.dump(state, f)
        os.replace(tmp_file, STATE_FILE)
    except Exception as e:
        pass # Silent fail to avoid spam

def extract_features(packet):
    duration = time.time() - start_time
    if TCP in packet: protocol = 1
    elif UDP in packet: protocol = 2
    elif ICMP in packet: protocol = 3
    else: protocol = 0
    src_bytes = len(packet)
    dst_bytes = len(packet)
    features = np.zeros(41)
    features[0] = duration
    features[1] = protocol
    features[4] = src_bytes
    features[5] = dst_bytes
    features[22] = total_packets 
    features[23] = total_packets 
    df = pd.DataFrame(features.reshape(1, -1), columns=columns)
    return df

def packet_handler(packet):
    global total_packets, total_attacks, current_status, last_attack_time, last_file_update

    now = time.time()
    total_packets += 1
    packet_times.append(now)
    
    # Initialize Throttle Timer
    if 'last_file_update' not in globals():
        last_file_update = 0

    # ---------------------------
    # 1. OPTIMIZED TRAFFIC ANALYSIS
    # ---------------------------
    is_http = False
    if TCP in packet:
        # Check ports (8080 focus)
        # Using simple integer set checking for speed
        if packet[TCP].dport == 8080 or packet[TCP].sport == 8080:
             is_http = True
             http_requests.append(now)

    # ---------------------------
    # 2. O(1) SLIDING WINDOW MAINTAINANCE
    # ---------------------------
    # Remove packets older than window from LEFT of deque
    while http_requests and http_requests[0] < (now - HTTP_WINDOW_SECONDS):
        http_requests.popleft()
        
    while packet_times and packet_times[0] < (now - 0.5):
        packet_times.popleft()

    # Current Counts (Instant access via len)
    http_count_window = len(http_requests)
    packet_rate = len(packet_times) # Rate per 1.0s (since update above)
    
    # Debug Print (Every ~50 packets)
    if total_packets % 50 == 0:
        print(f"DEBUG: Rate={packet_rate}/s | HTTP Queue={http_count_window}")
        sys.stdout.flush()

    # ---------------------------
    # 3. INSTANT DETECTION LOGIC
    # ---------------------------
    attack_detected = False
    attack_type = ""
    
    # RULE 1: HTTP Flood (Ultra-Sensitive)
    if http_count_window > HTTP_REQ_THRESHOLD:
        attack_detected = True
        attack_type = "HTTP/HTTPS Flood"
        print(f"🚨 [RULE] FLOOD! {http_count_window} reqs in {HTTP_WINDOW_SECONDS}s")
        sys.stdout.flush() # FORCE VISIBILITY

    # RULE 2: Generic Volumetric
    elif packet_rate > 200:
        attack_detected = True
        attack_type = "Volumetric TCP Flood"
        print(f"🚨 [RULE] HIGH TRAFFIC! {packet_rate} pkts/s")
        sys.stdout.flush()

    # RULE 3: ML (Asynchronous Check?) -> Keep it simple for speed
    elif model is not None and total_packets % 5 == 0: # Only check ML every 5th packet to save CPU
        try:
            features = extract_features(packet)
            prediction = model.predict(features)[0]
            if prediction == "attack": 
                attack_detected = True
                attack_type = "ML Anomaly Pattern"
                print("🚨 [ML] ANOMALY DETECTED")
                sys.stdout.flush()
        except:
            pass 

    # ---------------------------
    # 4. STATE UPDATE
    # ---------------------------
    if attack_detected:
        last_attack_time = now
        if current_status != "ATTACK":
            current_status = "ATTACK"
            total_attacks += 1
            log_attack(attack_type, max(http_count_window, packet_rate))
    
    else:
        # Cooldown
        if current_status == "ATTACK":
            time_since_last = now - last_attack_time
            if time_since_last > COOLDOWN_DURATION:
                current_status = "Normal"
                print("✅ [INFO] Attack subsided.")
                sys.stdout.flush()

    # Optimized File I/O
    # Update immediately on status change OR every 0.25s
    should_update = False
    if current_status != getattr(packet_handler, 'last_status', None): 
        should_update = True # Immediate update on state change
    elif (now - last_file_update) > 0.25:
        should_update = True
        
    if should_update:
        if len(packet) > 1:
            try: protocol_name = packet[1].name
            except: protocol_name = "Raw"
        else: protocol_name = "Unknown"
            
        last_feat_msg = f"Extracted 41 Features (Protocol={protocol_name}, Size={len(packet)}B)"
        model_stat = "Active (Random Forest)" if model else "Disabled"
        update_state_file(current_status, total_packets, total_attacks, last_features=last_feat_msg, model_status=model_stat)
        last_file_update = now
        packet_handler.last_status = current_status

# --- ENTRY POINT ---
print(f"🚀 [SYSTEM START] SecureNet AI IDS Initialized... (ULTRATHINK MODE)")
print(f"ℹ️  [CONFIG] Threshold: {HTTP_REQ_THRESHOLD} reqs within {HTTP_WINDOW_SECONDS}s")
print("📡 Listening on 'en0' and 'lo0'...")
print("Press Ctrl+C to stop")
sys.stdout.flush()

# Reset State
update_state_file("Normal", 0, 0, last_features="Initializing...", model_status="Loading...")

sniff(
    iface=["en0", "lo0"],   
    prn=packet_handler,
    store=False
)
