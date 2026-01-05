import streamlit as st
import json
import time
import os
import pandas as pd
from datetime import datetime

# -----------------------
# PAGE CONFIGURATION
# -----------------------
st.set_page_config(
    page_title="SecureNet AI | SOC Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit Default Elements
hide_gui_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        background-color: #050505;
        background-image: 
            radial-gradient(circle at 50% 50%, rgba(0, 240, 255, 0.03) 0%, transparent 50%),
            linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)),
            url("https://www.transparenttextures.com/patterns/carbon-fibre.png");
    }
    </style>
"""
st.markdown(hide_gui_style, unsafe_allow_html=True)

STATE_FILE = "ids_state.json"

# -----------------------
# UTILITY: DATA LOADING
# -----------------------
def read_state():
    if not os.path.exists(STATE_FILE):
        return {"total": 0, "attacks": 0, "status": "Normal", "last_features": "System Initializing...", "model_status": "Offline"}
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"total": 0, "attacks": 0, "status": "Normal", "last_features": "Read Error...", "model_status": "Unknown"}

# -----------------------
# PREMIUM CSS INJECTION
# -----------------------
st.markdown("""
<style>
    /* ---------------- IMPORTS ---------------- */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=JetBrains+Mono:wght@400;700&display=swap');

    /* ---------------- TYPOGRAPHY ---------------- */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #ffffff;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
    }
    
    p, div, span, label {
        font-family: 'JetBrains Mono', monospace;
        color: #e0e0e0;
    }

    /* ---------------- ACCENT COLORS ---------------- */
    :root {
        --neon-cyan: #00f0ff;
        --neon-magenta: #ff006e;
        --neon-green: #00ff88;
        --neon-red: #ff3b3b;
        --glass-bg: rgba(10, 10, 15, 0.7);
        --glass-border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* ---------------- COMPONENTS ---------------- */
    
    /* KPI CARDS */
    .kpi-card {
        background: var(--glass-bg);
        border: var(--glass-border);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.3);
        border: 1px solid var(--neon-cyan);
    }

    .kpi-title {
        color: #94a3b8;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 10px 0;
        color: white;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }

    /* STATUS PANEL */
    .status-panel {
        text-align: center;
        padding: 40px;
        border-radius: 16px;
        background: rgba(0,0,0,0.6);
        border: 1px solid #333;
        margin-top: 20px;
        margin-bottom: 20px;
        transition: all 0.5s ease;
    }

    .status-normal {
        border: 2px solid var(--neon-green);
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.2);
    }

    .status-attack {
        border: 2px solid var(--neon-red);
        animation: pulse-red 1.5s infinite;
    }

    @keyframes pulse-red {
        0% { box-shadow: 0 0 0 0 rgba(255, 59, 59, 0.7); }
        70% { box-shadow: 0 0 0 20px rgba(255, 59, 59, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 59, 59, 0); }
    }

    .status-text {
        font-family: 'Orbitron', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        margin: 0;
    }

    /* LOG PANEL */
    .log-panel {
        background: black;
        border: 1px solid #333;
        padding: 15px;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #00ff88;
        height: 150px;
        overflow-y: scroll;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.8);
    }

    /* SCANLINE EFFECT */
    .scanlines::before {
        content: " ";
        display: block;
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        z-index: 1000;
        background-size: 100% 2px, 3px 100%;
        pointer-events: none;
    }
    
    /* CUSTOM STREAMLIT ELEMENTS */
    div.stButton > button {
        background: transparent;
        border: 1px solid var(--neon-cyan);
        color: var(--neon-cyan);
        border-radius: 4px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background: var(--neon-cyan);
        color: black;
        box-shadow: 0 0 15px var(--neon-cyan);
    }
    
</style>
""", unsafe_allow_html=True)

# -----------------------
# LOGIC & STATE (UI SIDE)
# -----------------------
state = read_state()

# PPS Calculation (UI Side only, since backend updates every 250ms+)
if 'last_total' not in st.session_state:
    st.session_state['last_total'] = state['total']
    st.session_state['last_time'] = time.time()
    st.session_state['pps'] = 0

current_time = time.time()
time_diff = current_time - st.session_state['last_time']

# Update PPS every 1 second roughly
if time_diff >= 1.0:
    packet_diff = state['total'] - st.session_state['last_total']
    st.session_state['pps'] = int(packet_diff / time_diff)
    st.session_state['last_total'] = state['total']
    st.session_state['last_time'] = current_time

# -----------------------
# UI LAYOUT
# -----------------------

# 1. HEADER
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
<div style="border-bottom: 2px solid #00f0ff; padding-bottom: 10px; margin-bottom: 20px;">
<h1 style="margin:0; font-size: 2.2rem;">AI-AUGMENTED IDS <span style="font-size:1rem; color:#00f0ff; vertical-align:middle;"> // V1.0</span></h1>
<div style="color: #94a3b8; font-size: 0.9rem; letter-spacing: 2px;">REAL-TIME NETWORK THREAT SECURITY OPERATIONS CENTER</div>
</div>
""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
<div style="text-align: right; padding-top: 10px;">
<div style="color: var(--neon-cyan); font-weight: bold;">{datetime.now().strftime('%H:%M:%S')}</div>
<div style="font-size: 0.7rem; color: #666;">SYSTEM ONLINE</div>
</div>
""", unsafe_allow_html=True)

# 2. KPI METRICS (ROW 1)
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
<div class="kpi-card">
<div class="kpi-title">Total Packets</div>
<div class="kpi-value" style="color: var(--neon-cyan);">{state['total']:,}</div>
<div style="font-size: 0.7rem; color: #666;">CAPTURED</div>
</div>
""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
<div class="kpi-card">
<div class="kpi-title">Threats Blocked</div>
<div class="kpi-value" style="color: var(--neon-magenta);">{state['attacks']}</div>
<div style="font-size: 0.7rem; color: #666;">TOTAL DETECTIONS</div>
</div>
""", unsafe_allow_html=True)

with k3:
    pps = st.session_state['pps']
    color = "var(--neon-green)" if pps < 50 else "var(--neon-red)"
    st.markdown(f"""
<div class="kpi-card">
<div class="kpi-title">Traffic Rate</div>
<div class="kpi-value" style="color: {color};">{pps}</div>
<div style="font-size: 0.7rem; color: #666;">PACKETS / SEC (EST)</div>
</div>
""", unsafe_allow_html=True)

with k4:
    model_color = "#00ff88" if state['model_status'] == "Active (Random Forest)" else "#fbbf24"
    st.markdown(f"""
<div class="kpi-card">
<div class="kpi-title">AI Engine</div>
<div class="kpi-value" style="font-size: 1.2rem; margin-top: 25px; margin-bottom: 25px; color: {model_color};">
{state['model_status'].split(' ')[0]}
</div>
<div style="font-size: 0.7rem; color: #666;">MODEL: RANDOM FOREST</div>
</div>
""", unsafe_allow_html=True)

# 3. THREAT STATUS PANEL (CENTER)
status = state["status"]
if status == "ATTACK":
    status_class = "status-attack"
    status_color = "var(--neon-red)"
    status_msg = "⚠️ ALERT: ATTACK DETECTED"
    sub_msg = "TRAFFIC PATTERN MATCHES KNOWN THREAT SIGNATURE"
    # Audio Alert integration
    st.markdown("""
        <audio autoplay>
        <source src="https://assets.mixkit.co/sfx/preview/mixkit-alarm-digital-clock-beep-989.mp3" type="audio/mpeg">
        </audio>
    """, unsafe_allow_html=True)
else:
    status_class = "status-normal"
    status_color = "var(--neon-green)"
    status_msg = "🛡️ SYSTEM NORMAL"
    sub_msg = "NO ACTIVE THREATS DETECTED"

st.markdown(f"""
<div class="status-panel {status_class}">
<div class="status-text" style="color: {status_color};">{status_msg}</div>
<div style="margin-top: 10px; color: #fff; opacity: 0.8; letter-spacing: 2px;">{sub_msg}</div>
</div>
""", unsafe_allow_html=True)


# 4. LOWER SECTION: DETAILS & FEATURES
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("### 📡 LIVE TRAFFIC ANALYSIS")
    st.markdown(f"""
<div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; border: 1px solid #333;">
<div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
<span style="color: #666;">LAST EXTRACTED FEATURE VECTOR:</span>
<span style="color: var(--neon-cyan);">ID: {state['total']}</span>
</div>
<div style="font-family: 'JetBrains Mono'; font-size: 0.85rem; color: #e0e0e0; line-height: 1.6;">
> {state['last_features']}
</div>
<div style="margin-top: 15px; display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
<div>
<span style="color: #666; font-size: 0.8rem;">PROTOCOL</span><br>
{"TCP/IP" if "TCP" in state['last_features'] else "UDP/OTHER"}
</div>
<div>
<span style="color: #666; font-size: 0.8rem;">INTERFACE</span><br>
EN0 (WI-FI)
</div>
</div>
</div>
""", unsafe_allow_html=True)

with c2:
    st.markdown("### ⚙️ SYSTEM STATE")
    st.markdown("""
<div style="background: rgba(0,0,0,0.5); padding: 10px; border-radius: 6px; font-size: 0.8rem;">
<div style="display:flex; justify-content:space-between; margin-bottom:5px;">
<span>CAPTURE ENGINE</span> <span style="color: #00ff88;">● ONLINE</span>
</div>
<div style="display:flex; justify-content:space-between; margin-bottom:5px;">
<span>ML INFERENCE</span> <span style="color: #00ff88;">● ONLINE</span>
</div>
<div style="display:flex; justify-content:space-between; margin-bottom:5px;">
<span>STATE SYNC</span> <span style="color: #00ff88;">● 0.5s</span>
</div>
<div style="display:flex; justify-content:space-between;">
<span>DASHBOARD</span> <span style="color: #00f0ff;"> V1.0.4 PREMIUM</span>
</div>
</div>
""", unsafe_allow_html=True)
    
    st.write("")
    if st.button("RELOAD SYSTEM"):
        st.cache_data.clear()
        st.rerun()

# 5. FOOTER
st.markdown("""
<div style="position: fixed; bottom: 10px; right: 20px; text-align: right; opacity: 0.5; font-size: 0.7rem;">
FINAL YEAR PROJECT // SECURITY OPERATIONS<br>
DESIGNED BY LAKSHITHA MADUSHAN & BINARA NETHSARA
</div>
""", unsafe_allow_html=True)

# Scanline overlay div (Must be last)
st.markdown('<div class="scanlines"></div>', unsafe_allow_html=True)

# Auto-Refresh Logic
time.sleep(0.5)
st.rerun()
