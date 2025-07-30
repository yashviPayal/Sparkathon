# Walmart Sparkathon
**Building Trust with Cybersecurity**

**Team CodeCrafters**

An **AI-driven e-commerce security platform** to detect **fraudulent transactions, bot activities, behavioral anomalies, and security threats** in real-time. Designed for digital retailers to enhance trust, prevent cyber-attacks, and ensure safe transactions through intelligent monitoring dashboards.

---

## Project Features

* 🔊 **Real-Time Fraud & Security Detection** using AI models.
* 🛡️ **Bot Detection & Behavioral Anomaly Identification**.
* 🔒 **Role-Based Dashboards (User/Admin Views)**.
* 📧 **Automated Order Confirmation Emails**.
* 📊 **Live Session Monitoring with Auto-Refresh & Alerts**.
* 📂 **CSV-Based Data Handling (Purchase History, Live Predictions)**.

---

## 🛠Tech Stack

| Layer         | Technologies                                                  |
| ------------- | ------------------------------------------------------------- |
| **Frontend**  | Streamlit, streamlit-extras, Session State                    |
| **Backend**   | Python, Pandas, smtplib (email service)                       |
| **AI Models** | scikit-learn (pkl models for fraud, bot, behavior & security) |
| **Storage**   | CSV Files (Scalable to Databases)                             |

---

## Installation

```bash
# Clone Repository
git clone <repo_url>
cd spark_ai

# Create Virtual Environment
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Ensure secrets.toml exists at: ~/.streamlit/secrets.toml

# Run Streamlit App
streamlit run app.py
```

---

## Project Folder Structure

```
.
├── ai_models/
│   └── ai_agent.py
├── utils/
│   └── auth.py
├── model/
│   ├── fraud_model.pkl
│   ├── security_model.pkl
│   └── ... (all .pkl models)
├── data/
│   ├── purchase_history.csv
│   ├── live_predictions.csv
│   └── centralized_behavior_fraud_security_dataset.csv
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Login.py
│   ├── 3_Register.py
│   ├── 4_User_Dashboard.py
│   └── 5_Admin_Dashboard.py
├── app.py
├── requirements.txt
└── README.md
```

---

## Usage Instructions

1. **Admin Login**

   * Access the Admin Dashboard.
   * Upload CSV files for batch predictions.
   * Monitor real-time sessions for live fraud alerts.

2. **User Dashboard**

   * Browse & purchase items.
   * AI models will analyze every transaction for fraud.
   * Get real-time anomaly detection results.

3. **Data Flow**

   * Purchase data updates `purchase_history.csv`.
   * AI Predictions log into `live_predictions.csv`.
   * Admin Dashboard auto-refreshes to show live fraud attempts.

---

## Future Enhancements

* Integrate Database Systems (MongoDB/PostgreSQL)
* Live Session Replay & Heatmap Analytics
* Biometric Authentication & Zero-Trust Framework
* Scalable Cloud Deployment (Docker/Kubernetes)
* Self-Learning AI Pipelines with Feedback Loops

---

## About

This project aligns with the theme: **"Building Trust in Retail with Cybersecurity"**, delivering a robust AI-powered solution to prevent fraud, enhance real-time monitoring, and protect consumer confidence in e-commerce platforms.

---

## Demo Video

https://youtu.be/thONGsnqD5A
---

## Connect & Contributions

We welcome contributions, enhancements, and suggestions. Feel free to fork the repo, raise issues, or contact us for collaboration.

---
