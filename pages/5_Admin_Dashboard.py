import streamlit as st
import pandas as pd
import os
from ai_models.ai_agent import run_full_predictions
from utils.auth import verify_login, save_user
from streamlit.runtime.scriptrunner.script_runner import RerunException
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx

# ----------------------------
# 🔁 Auto-refresh every 5 seconds
# ----------------------------
st_autorefresh(interval=5000, key="data_refresh")

# ----------------------------
# 🔐 Access Control
# ----------------------------
st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.title("🛠️ Admin Dashboard")

if not st.session_state.get("logged_in"):
    st.warning("🔒 Please log in.")
    st.stop()

if st.session_state.get("role") != "admin":
    st.error("⛔ Access denied. This page is for admins only.")
    st.stop()

st.success(f"✅ Welcome, Admin: {st.session_state.get('username')}")

# ----------------------------
# 🚪 Logout Button
# ----------------------------
if st.button("🚪 Logout"):
    for key in ["logged_in", "username", "role", "email", "phone"]:
        st.session_state.pop(key, None)
    ctx = get_script_run_ctx()
    if ctx is not None:
        raise RerunException(ctx)
# ----------------------------
# 📤 Upload CSV for Prediction
# ----------------------------
st.subheader("🔍 Upload Session/Transaction Data")
uploaded_file = st.file_uploader("Upload CSV containing session and transaction data", type="csv")

df_pred = None

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # ✅ Rename user_id → username if needed
        if 'user_id' in df.columns and 'username' not in df.columns:
            df.rename(columns={"user_id": "username"}, inplace=True)

        st.write("📋 Uploaded Data Sample:")
        st.dataframe(df.head())

        if st.button("🧠 Run All Predictions"):
            with st.spinner("Running AI models..."):
                predictions_list = []
                for _, row in df.iterrows():
                    try:
                        prediction = run_full_predictions(row.to_dict())
                        row_data = row.to_dict()
                        row_data.update({
                            "is_fraud_predicted": prediction["fraud"],
                            "is_behavior_anomalous": prediction["behavior"],
                            "is_bot_predicted": prediction["bot"],
                            "is_security_threat_predicted": prediction["security_threat"]
                        })
                        predictions_list.append(row_data)
                    except Exception as e:
                        st.warning(f"⚠️ Skipped row due to error: {e}")

                df_pred = pd.DataFrame(predictions_list)

            st.success("✅ All Predictions Complete!")

            # ----------------------------
            # 📊 Results Section
            # ----------------------------
            st.subheader("📊 Fraud Predictions")
            st.dataframe(df_pred[['username', 'purchase_amount', 'is_fraud_predicted']])

            st.subheader("🔐 Security Alerts")
            st.dataframe(df_pred[['username', 'failed_login_attempts', 'geo_location_mismatch', 'is_security_threat_predicted']])

            st.subheader("🧠 Behavior Overview")
            st.dataframe(df_pred[['username', 'typing_time', 'click_count', 'is_behavior_anomalous']])

            st.subheader("🤖 Bot Detection Overview")
            st.dataframe(df_pred[['username', 'user_agent_contains_bot', 'navigator_webdriver', 'is_bot_predicted']])

            # 📥 CSV Download
            csv = df_pred.to_csv(index=False).encode("utf-8")
            st.download_button("⬇ Download Full Prediction CSV", csv, "prediction_results.csv", "text/csv")

    except Exception as e:
        st.error(f"⚠️ Error while processing uploaded file: {e}")

# ----------------------------
# 📡 Real-Time User Sessions + Fraud Alerts
# ----------------------------
st.subheader("📡 Real-Time User Sessions")

live_file = "data/live_predictions.csv"
live_df = None

if os.path.exists(live_file):
    try:
        live_df = pd.read_csv(live_file)

        if not live_df.empty:
            st.dataframe(live_df.sort_values("timestamp", ascending=False))

            # 🚨 Alert for new frauds
            recent_fraud = live_df[live_df["is_fraud_predicted"] == 1]
            if not recent_fraud.empty:
                st.warning(f"🚨 {len(recent_fraud)} new fraud attempt(s) detected in live data.")
                st.dataframe(recent_fraud.sort_values("timestamp", ascending=False).head(3))

            st.line_chart(live_df[["is_bot_predicted", "is_behavior_anomalous"]].rolling(5).mean())

        else:
            st.info("🟡 Live data available but empty.")
    except Exception as e:
        st.error(f"📛 Error reading live data: {e}")
else:
    st.info("⏳ No live_predictions.csv yet.")

# ----------------------------
# 📈 Daily Anomaly Summary
# ----------------------------
st.subheader("📈 Daily Anomaly Summary")

# Use df_pred (uploaded + processed) or fallback to live_df
df_source = df_pred if df_pred is not None else live_df

if df_source is not None and not df_source.empty:
    try:
        df_source['timestamp'] = pd.to_datetime(df_source['timestamp'])
        df_source['date'] = df_source['timestamp'].dt.date

        daily_summary = df_source.groupby("date").agg({
            "is_fraud_predicted": "sum",
            "is_security_threat_predicted": "sum",
            "is_bot_predicted": "sum",
            "is_behavior_anomalous": "sum"
        }).reset_index()

        st.dataframe(daily_summary)
        st.area_chart(daily_summary.set_index("date"))

    except Exception as e:
        st.warning(f"Report error: {e}")
else:
    st.info("📭 No data available for anomaly summary.")
