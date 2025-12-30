# AI-AUGMENTED REAL-TIME IDS (v1.0) 🛡️

**A High-Performance Network Intrusion Detection System using Machine Learning and O(1) Traffic Analysis.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![Scikitlearn](https://img.shields.io/badge/AI-Random_Forest-orange)
![Scapy](https://img.shields.io/badge/Network-Scapy-green)

---

## 🚀 Project Overview
This project is an **AI-Augmented Real-Time Intrusion Detection System (IDS)** designed to detect network attacks (DoS, DDoS, Port Scans, Web Floods) instantly. 

It combines **Rule-Based Speed** (for volumetric attacks) with **Machine Learning Intelligence** (Random Forest trained on CICIDS2017) to provide a robust defense mechanism with **<1.0s detection latency**.

### 🔑 Key Features
1.  **Real-Time Packet Capture**: Listens to live traffic on `en0` (Wi-Fi) and `lo0` (Loopback).
2.  **Ultrathink Engine (O(1))**: Uses optimized `deque` logic to process packets with zero CPU lag.
3.  **AI integration**: Extracts **41 Features** per packet and classifies them using a trained **Random Forest** model.
4.  **Live Dashboard**: A "Sci-Fi" style dashboard (Streamlit) that updates 2x/second.

---

## 🛠️ System Architecture (The 4 Modules)

The system is built on a strictly modular pipeline:

1.  **Packet Capture Module** (`realtime_ids.py`)
    *   *Function:* Captures raw binary packets from the network interface.
2.  **Feature Extraction Module** (`realtime_ids.py`)
    *   *Function:* Converts raw packets into a structured vector of 41 mathematical features (Duration, Bytes, Flags, etc.).
3.  **AI Detection Module** (`models/rf_ids_model.pkl`)
    *   *Function:* A Random Forest Classifier that predicts "Attack" or "Normal" based on the feature vector.
4.  **Real-Time Detection Engine** (`realtime_ids.py` loop)
    *   *Function:* A sliding-window logic that monitors traffic rates (HTTP Floods) and enforces thresholds (e.g., >10 req/s on Port 8080).

---

## ⚡ Performance Metrics
*   **Detection Window:** 1.0 Second
*   **Cooldown:** 0.1s (Instant Recovery)
*   **UI Refresh Rate:** 500ms (2 FPS)
*   **Target Port:** Optimized for Port 8080 (Web Traffic)

---

## 🖥️ How to Run

### prerequisites
*   macOS / Linux
*   Python 3.9+
*   `libpcap` (usually pre-installed on macOS)

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/Madushan186/AI-Augmented-Real-Time-IDS-v1.0-.git
cd AI-Augmented-Real-Time-IDS-v1.0-

# Install dependencies
pip install -r requirements.txt
```

### 2. Start the System
We use a unified launcher script to start the Detection Engine, Dashboard, and Dummy Server properly.

```bash
sudo ./run_ids.sh
```
*(Sudo is required to capture network packets)*

---

## 🧪 Testing Attacks
The system comes with a built-in simulation tool.

1.  **Start the IDS** (`sudo ./run_ids.sh`)
2.  **Run the PowerShell Attack Simulation** (from a Windows machine or compatible shell):
    ```powershell
    # Simulates an HTTP Flood on Port 8080
    for($i=0; $i -lt 500; $i++) { Invoke-WebRequest http://YOUR_MAC_IP:8080 }
    ```
3.  **Observe**: The Dashboard strips turn **RED** instantly with an audio alert.

---

## 📂 File Structure
*   `realtime_ids.py`: **The Brain**. Handles capture, ML config, and detection logic.
*   `dashboard.py`: **The Face**. Streamlit UI code.
*   `dummy_server.py`: **The Trap**. Opens Port 8080 to receive test traffic.
*   `run_ids.sh`: **The Launcher**. Orchestrates the multi-process startup.

---

**Author:** Lakshitha Madushan
**Project Type:** Final Year Project (Cybersecurity/AI)
