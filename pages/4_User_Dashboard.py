import streamlit as st
import pandas as pd
import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ai_models.ai_agent import run_full_predictions
from utils.auth import verify_login, save_user
from streamlit.runtime.scriptrunner.script_runner import RerunException
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx

# ----------------------------
# 🔐 Role-Based Access Control
# ----------------------------
st.set_page_config(page_title="User Dashboard", layout="wide")
st.title("🛍️ User Dashboard")

if not st.session_state.get("logged_in"):
    st.warning("🔒 You must be logged in.")
    st.stop()

if st.session_state.get("role") != "user":
    st.error("⛔ Access denied. This page is for users only.")
    st.stop()

st.success(f"Welcome, {st.session_state.get('username')} 👋")

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
# 🛒 Shop Items
# ----------------------------
st.header("🏍️ Shop Items")

products = [
    {"name": "Wireless Headphones", "price": 1200},
    {"name": "Smartwatch", "price": 2499},
    {"name": "Bluetooth Speaker", "price": 999},
    {"name": "Phone Case", "price": 299},
    {"name": "Power Bank", "price": 699}
]

if "cart" not in st.session_state:
    st.session_state.cart = []

cols = st.columns(2)
for i, product in enumerate(products):
    with cols[i % 2]:
        st.subheader(product["name"])
        st.write(f"💰 Price: ₹{product['price']}")
        qty_key = f"qty_{product['name']}"
        quantity = st.number_input(f"Quantity for {product['name']}", 1, 10, 1, key=qty_key)
        if st.button(f"Add to Cart: {product['name']}", key=product["name"]):
            st.session_state.cart.append({
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity
            })

# ----------------------------
# 🛒 Cart and Checkout
# ----------------------------
if st.session_state.cart:
    st.subheader("🛒 Your Cart")
    cart_df = pd.DataFrame(st.session_state.cart)
    cart_df["total"] = cart_df["price"] * cart_df["quantity"]
    st.dataframe(cart_df)

    total = cart_df["total"].sum()
    st.success(f"📿 Total: ₹{total}")

    payment_method = st.selectbox("💳 Choose Payment Method", ["Credit Card", "Debit Card", "UPI", "Cash on Delivery"])

    if st.button("✅ Place Order"):
        order_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save purchase data
        df_to_save = cart_df.copy()
        df_to_save["username"] = st.session_state.get("username")
        df_to_save["timestamp"] = order_time
        df_to_save["payment_method"] = payment_method

        file_path = "data/purchase_history.csv"
        file_exists = os.path.exists(file_path)
        df_to_save.to_csv(file_path, mode='a', index=False, header=not file_exists)

        # 📧 Send Confirmation Email
        user_email = st.session_state.get("email")
        if user_email:
            try:
                sender_email = st.secrets["email_sender"]
                app_password = st.secrets["email_password"]

                msg = MIMEMultipart("alternative")
                msg["Subject"] = "🛒 Order Confirmation"
                msg["From"] = sender_email
                msg["To"] = user_email
                text = f"Hi {st.session_state['username']},\n\nYour order of ₹{total} has been placed successfully on {order_time} using {payment_method}.\n\nThank you for shopping with us!"
                msg.attach(MIMEText(text, "plain"))

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(sender_email, app_password)
                    server.sendmail(sender_email, user_email, msg.as_string())

                st.success("📧 Confirmation email sent!")
            except Exception as e:
                st.error(f"Email error: {e}")

        # Anomaly Detection: Rule-based
        item_counts = df_to_save['name'].value_counts()
        for item, count in item_counts.items():
            if count >= 5:
                st.warning(f"⚠️ Anomaly Detected: {count} units of '{item}' in one order.")

        # 🧠 AI-Based Prediction
        st.subheader("🧠 AI Fraud & Security Detection")

        session_input = {
            'typing_time': 1.3,
            'paste_detected': 0,
            'mouse_moves_per_second': 4.5,
            'scroll_depth': 80,
            'total_time_on_page': 260,
            'keystroke_variance': 0.05,
            'click_count': 22,
            'mouse_click_rate': 0.085,
            'idle_time_ratio': 0.2,
            'hover_time': 35,
            'scroll_velocity': 6.7,
            'user_agent_contains_bot': 0,
            'navigator_webdriver': 0,
            'js_enabled': 1,
            'cookie_enabled': 1,
            'purchase_amount': total,
            'num_items': cart_df["quantity"].sum(),
            'account_age_days': 150,
            'session_duration': 260,
            'failed_login_attempts': 0,
            'geo_location_mismatch': 0,
            'timezone_mismatch': 0,
            'multiple_sessions_same_ip': 0,
            'account_takeover_risk': 0,
            'sudden_ip_change': 0,
            'captcha_triggered': 0
        }

        try:
            predictions = run_full_predictions(session_input)
            st.info(f"🧠 Behavior Detection: {'⚠️ Anomalous' if predictions['behavior'] else '✅ Normal'}")
            st.info(f"🤖 Bot Detection: {'🚨 Bot Detected' if predictions['bot'] else '✅ Human'}")
            st.info(f"🛡️ Fraud Detection: {'🚨 Fraudulent' if predictions['fraud'] else '✅ Safe'}")
            st.info(f"🔐 Security Threat: {'🚨 Threat Detected' if predictions['security_threat'] else '✅ Secure'}")
        except Exception as e:
            st.error(f"Prediction error: {e}")

        # Save live prediction with all 4 labels
        live_df = pd.DataFrame([{
            "username": st.session_state["username"],
            "timestamp": order_time,
            "typing_time": session_input["typing_time"],
            "click_count": session_input["click_count"],
            "total_time_on_page": session_input["total_time_on_page"],
            "is_bot_predicted": predictions["bot"],
            "is_behavior_anomalous": predictions["behavior"],
            "is_fraud_predicted": predictions["fraud"],
            "is_security_threat_predicted": predictions["security_threat"]
        }])

        live_file = "data/live_predictions.csv"
        if os.path.exists(live_file):
            old = pd.read_csv(live_file)
            live_df = pd.concat([old, live_df], ignore_index=True)

        live_df.to_csv(live_file, index=False)

        # Clear cart
        st.session_state.cart = []

else:
    st.info("🛒 Your cart is empty.")

# ----------------------------
# 📦 Past Orders
# ----------------------------
st.header("📦 Your Past Orders")
try:
    df_history = pd.read_csv("data/purchase_history.csv")
    df_user_orders = df_history[df_history["username"] == st.session_state["username"]]
    if not df_user_orders.empty:
        st.dataframe(df_user_orders.sort_values("timestamp", ascending=False))
    else:
        st.info("No past orders found.")
except FileNotFoundError:
    st.info("No order history available yet.")
