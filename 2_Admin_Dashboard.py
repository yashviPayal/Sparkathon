#2_Admin_Dashboard.py
import streamlit as st
import pandas as pd
from utils.fraud_model import predict_fraud
from utils.isolation_forest_model import run_isolation_forest

st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.title("🛠️ Admin Dashboard")

# 🔒 Role check
if not st.session_state.get("logged_in") or st.session_state.get("role") != "admin":
    st.warning("⛔ Admin access only. Please log in with an admin account.")
    st.stop()

# 👤 Welcome
st.success(f"Welcome, Admin: {st.session_state.get('username')}")

# -------------------------
# 🔍 Model Selection Panel
# -------------------------
st.subheader("📥 Upload Data for Analysis")

# Step 1: Choose which model to run
model_type = st.selectbox("Select model to run:", [
    "Fraud Detection (Categorical features)",
    "Anomaly Detection (Isolation Forest)"
])

# Step 2: Upload the data file
uploaded_file = st.file_uploader("Upload .CSV file (transaction/order data)", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("📋 Uploaded Data Sample:")
        st.dataframe(df.head())

        # ========== FRAUD DETECTION ==========
        if model_type == "Fraud Detection (Categorical features)":
            required_columns = [
                'payment_method', 'login_location', 'device_type', 'browser_os',
                'cookie_behavior', 'session_token_behavior', 'email_reputation'
            ]
            missing_cols = [col for col in required_columns if col not in df.columns]

            if missing_cols:
                st.error(f"❌ Missing required columns for fraud detection: {', '.join(missing_cols)}")
            else:
                if st.button("🧠 Run Fraud Detection"):
                    with st.spinner("Analyzing transactions for fraud..."):
                        try:
                            result_df = predict_fraud(df)
                            st.success("✅ Fraud Prediction Complete!")
                            st.subheader("🧾 Prediction Results:")
                            st.dataframe(result_df)

                            csv = result_df.to_csv(index=False).encode("utf-8")
                            st.download_button("⬇ Download Fraud Prediction CSV", csv, "fraud_results.csv", "text/csv")

                        except Exception as e:
                            st.error(f"⚠️ Error during fraud prediction: {e}")

        # ========== ISOLATION FOREST ANOMALY DETECTION ==========
        elif model_type == "Anomaly Detection (Isolation Forest)":
            required_columns_if = ['order_id', 'order_hour_of_day', 'reordered', 'user_id']
            missing_cols_if = [col for col in required_columns_if if col not in df.columns]

            if missing_cols_if:
                st.error(f"❌ Missing required columns for anomaly detection: {', '.join(missing_cols_if)}")
            else:
                if st.button("🔍 Run Anomaly Detection"):
                    with st.spinner("Running Isolation Forest anomaly detection..."):
                        try:
                            anomaly_results = run_isolation_forest(df)
                            st.success("✅ Anomaly Detection Complete!")
                            st.subheader("🧾 Anomaly Detection Results (per user):")
                            st.dataframe(anomaly_results)

                            csv = anomaly_results.to_csv(index=False).encode("utf-8")
                            st.download_button("⬇ Download Anomaly Results CSV", csv, "anomaly_results.csv", "text/csv")

                        except Exception as e:
                            st.error(f"⚠️ Error during anomaly detection: {e}")

    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")
