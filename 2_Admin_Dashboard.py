import streamlit as st
import pandas as pd
from utils.fraud_model import predict_fraud  # ✅ your real-time prediction logic

st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.title("🛠️ Admin Dashboard")

# 🔒 Role check
if not st.session_state.get("logged_in") or st.session_state.get("role") != "admin":
    st.warning("⛔ Admin access only. Please log in with an admin account.")
    st.stop()

# 👤 Welcome
st.success(f"Welcome, Admin: {st.session_state.get('username')}")

# -------------------------
# 📥 Upload CSV for Fraud Detection
# -------------------------
st.subheader("🔍 Fraud Detection Panel")
uploaded_file = st.file_uploader("Upload transaction data (.csv)", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("📋 Uploaded Data Sample:")
        st.dataframe(df.head())

        if st.button("🧠 Run Fraud Detection"):
            with st.spinner("Analyzing transactions..."):
                result_df = predict_fraud(df)
                st.success("✅ Prediction Complete!")

                # Display results
                st.subheader("🧾 Prediction Results:")
                st.dataframe(result_df)

                # Download button
                csv = result_df.to_csv(index=False).encode("utf-8")
                st.download_button("⬇ Download Result CSV", csv, "fraud_results.csv", "text/csv")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
