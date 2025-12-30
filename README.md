# AI Real-Time Intrusion Detection System (IDS)

## 📌 Project Overview (Phase 1: Alpha)
This project implements the **Core Engine** of a Real-Time AI-based Intrusion Detection System (IDS). 
Currently, **Phase 1 (50% Completion)** is implemented, which includes:
- **Packet Sniffing**: Live network capture on `en0`.
- **Traffic Analysis**: Rule-based detection for HTTP Floods.
- **Supervised AI**: Random Forest model for known attack patterns.

Severe detected threats are visualized on a **Real-Time Dashboard**.

> **Note**: Advanced features like Unsupervised Learning (Isolation Forest) and Automated Retraining are scheduled for **Phase 2**.

---

## 🗺️ Roadmap / Future Work (Phase 2)
The following features are designed but **currently disabled** or **under development**:

- [ ] **Unsupervised Anomaly Detection**: Integration of Isolation Forest for zero-day threats.
- [ ] **Automated Model Retraining**: Pipeline to update AI models with new attack data.
- [ ] **Database Persistence**: SQLite integration for long-term historical logs.
- [ ] **Detailed Reporting**: PDF export of attack sessions.

---

## 🚀 Quick Start Guide (Phase 1)

### 1️⃣ How to Start
The easiest way to run the entire system (Detection Engine + Dashboard) is using the helper script:

```bash
sudo ./run_ids.sh
```

**Manual Start (Alternative):**
If you prefer to run components separately in two terminals:

**Terminal 1 (Detection Engine):**
```bash
sudo python3 realtime_ids.py
```

**Terminal 2 (Dashboard):**
```bash
streamlit run dashboard.py
```

---

### 2️⃣ How to Stop
To safely stop the system:

1.  **Press `Ctrl + C`** in the terminal where the script is running.
2.  If you ran the components separately, go to **both** terminals and press `Ctrl + C`.

The system handles shutdown gracefully:
- Logs are saved.
- Network sniffers are released.
- File handles are closed.

---

## 🧪 Simulation
To test the detection capabilities, run the attack simulator in a separate terminal:

```bash
sudo python3 simulate_attack.py
```
This sends harmless packets that mimic an HTTP Flood attack to trigger the system.

---

## 🧠 System Architecture (Hybrid AI)
1.  **Victim Server**: Python HTTP Server running on `Port 8080`.
2.  **Traffic Analysis (Rules)**: Detects high-volume DoS attacks (>20 req/s).
3.  **Random Forest (Supervised AI)**: Detects known attack patterns (SQLi, Brute Force).
4.  **Isolation Forest (Unsupervised AI)**: Detects zero-day anomalies.
5.  **Dashboard**: Visualizes Confidence, Severity, and Detection Source.

---

## 🛠️ Technologies Used
- **Python 3**
- **Scapy** (Packet Capture)
- **Scikit-learn** (AI Models)
- **Streamlit** (Dashboard)
- **Pandas / NumPy** (Data Processing)

---

## 📂 Project Structure
- `realtime_ids.py`: Main detection engine.
- `dashboard.py`: Visualization interface.
- `simulate_attack.py`: Attack testing tool.
- `training/train_model.py`: Script to retrain AI models.
- `models/`: Stores `rf_ids_model.pkl` and `iso_forest.pkl`.
- `data/`: Contains KDDTrain+ dataset.
