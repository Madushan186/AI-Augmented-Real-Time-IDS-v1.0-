import streamlit as st
import json
import pandas as pd
import time
import os
import plotly.express as px

# -----------------------
# PAGE CONFIGURATION
# -----------------------
st.set_page_config(
    page_title="AI IDS Project",
    layout="wide"
)

# Hide Streamlit "3 dots" menu and footer
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_menu_style, unsafe_allow_html=True)

STATE_FILE = "ids_state.json"
LOG_FILE = "attack_log.csv"

# -----------------------
# DATA LOADING
# -----------------------
def read_state():
    if not os.path.exists(STATE_FILE):
        return {"total": 0, "attacks": 0, "status": "Normal", "last_features": "Waiting...", "model_status": "Unknown"}
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"total": 0, "attacks": 0, "status": "Normal", "last_features": "Waiting...", "model_status": "Unknown"}

# -----------------------
# MAIN APP
# -----------------------
state = read_state()

# Custom CSS for "Best Colour" (Vibrant Dark Mode)
st.markdown("""
<style>
    /* Global Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #ffffff;
    }

    /* Background */
    .stApp {
        background-color: #050505; /* Deep Black */
    }

    /* Section Headers */
    h3 {
        font-weight: 700 !important;
        margin-bottom: 10px !important;
    }

    /* Module Card Containers */
    .module-card {
        background: #121212;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }

    /* Status Pill Base */
    .status-pill {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# TITLE HEADER
# =========================================================
st.markdown("<h1 style='text-align: center; color: white; margin-bottom: 30px;'>AI-AUGMENTED REAL-TIME IDS</h1>", unsafe_allow_html=True)


# =========================================================
# 1. Real-Time Packet Capture Module
# =========================================================
st.markdown("<h3 style='color: #38bdf8;'>Real-Time Packet Capture Module</h3>", unsafe_allow_html=True)
st.markdown(f"""
<div class="module-card" style="border-left: 4px solid #38bdf8;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <div style="font-size: 0.9rem; color: #94a3b8;">Interface: <span style="color: white; font-weight: bold;">en0 (Wi-Fi)</span></div>
            <div style="font-size: 0.8rem; color: #4ade80; margin-top: 5px;">● Capture Active</div>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 2rem; font-weight: 700; color: #38bdf8;">{state['total']}</div>
            <div style="font-size: 0.8rem; color: #94a3b8;">Total Packets Captured</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# 2. Feature Extraction & Preprocessing
# =========================================================
st.markdown("<h3 style='color: #c084fc;'>Feature Extraction & Preprocessing</h3>", unsafe_allow_html=True)
features_text = state.get("last_features", "Initializing...")
# Use a cleaner code block look
st.markdown(f"""
<div class="module-card" style="border-left: 4px solid #c084fc;">
    <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 10px;">Last Extracted Feature Vector:</div>
    <div style="background: #1e1e1e; padding: 10px; border-radius: 6px; font-family: monospace; color: #e879f9; font-size: 0.85rem; border: 1px solid #333;">
        {features_text}
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# 3. Initial AI-Based Intrusion Detection Model
# =========================================================
st.markdown("<h3 style='color: #facc15;'>Initial AI-Based Intrusion Detection Model</h3>", unsafe_allow_html=True)
model_status = state.get("model_status", "Active")
st.markdown(f"""
<div class="module-card" style="border-left: 4px solid #facc15;">
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px;">
        <div>
            <div style="font-size: 0.8rem; color: #94a3b8;">Model Architecture</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: white;">Random Forest</div>
        </div>
        <div>
             <div style="font-size: 0.8rem; color: #94a3b8;">Status</div>
             <div style="font-size: 1.1rem; font-weight: 600; color: #4ade80;">{model_status}</div>
        </div>
        <div>
             <div style="font-size: 0.8rem; color: #94a3b8;">Training Dataset</div>
             <div style="font-size: 1.1rem; font-weight: 600; color: white;">CICIDS2017</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# 4. Real-Time Detection Engine
# =========================================================
st.markdown("<h3 style='color: #4ade80;'>Real-Time Detection Engine</h3>", unsafe_allow_html=True)

status = state["status"]
if status == "ATTACK":
    bg_color = "rgba(239, 68, 68, 0.2)"
    border_color = "#ef4444"
    text_color = "#ef4444"
    status_text = "⚠️ ATTACK DETECTED"
    animate = "animation: pulse 2s infinite;"
    st.audio("https://upload.wikimedia.org/wikipedia/commons/3/3a/Jungle_atmosphere_late_afternoon.ogg", format="audio/ogg")
else:
    bg_color = "rgba(74, 222, 128, 0.1)"
    border_color = "#4ade80"
    text_color = "#4ade80"
    status_text = "🛡️ NORMAL TRAFFIC"
    animate = ""

st.markdown(f"""
<style>
@keyframes pulse {{
    0% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }}
    70% {{ box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }}
}}
</style>
<div class="module-card" style="border: 2px solid {border_color}; background: {bg_color}; text-align: center; {animate}">
    <h2 style="color: {text_color}; margin: 0; font-size: 2.2rem; letter-spacing: 2px;">{status_text}</h2>
    <p style="color: #94a3b8; margin-top: 10px; font-size: 0.9rem;">Real-Time Logic: Basic Version Active</p>
</div>
""", unsafe_allow_html=True)


# Auto-Refresh
time.sleep(0.5)
st.rerun()
