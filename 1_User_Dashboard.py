#1_User_Dashboard.py
import streamlit as st
import pandas as pd
import datetime
import os
from utils.fraud_model import predict_fraud  # Optional fraud check

st.set_page_config(page_title="User Dashboard", layout="wide")

# 🔒 Auth check
if not st.session_state.get("logged_in") or st.session_state.get("role") != "user":
    st.warning("⛔ User access only. Please log in with a user account.")
    st.stop()

st.success(f"Welcome, {st.session_state.get('username')} 👋")

# ---------------------
# 🏍️ Product Catalog
# ---------------------
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
        quantity = st.number_input(
            f"Select quantity for {product['name']}",
            min_value=1,
            max_value=10,
            step=1,
            key=f"qty_{product['name']}"
        )
        if st.button(f"Add to Cart: {product['name']}", key=product["name"]):
            # Check if item already in cart, then update quantity
            existing = next((item for item in st.session_state.cart if item["name"] == product["name"]), None)
            if existing:
                existing["quantity"] += quantity
            else:
                st.session_state.cart.append({
                    "name": product["name"],
                    "price": product["price"],
                    "quantity": quantity
                })

# ---------------------
# 🛒 Cart Summary
# ---------------------
if st.session_state.cart:
    st.subheader("🛒 Your Cart")
    cart_df = pd.DataFrame(st.session_state.cart)
    cart_df["total"] = cart_df["price"] * cart_df["quantity"]
    st.dataframe(cart_df)

    total = cart_df["total"].sum()
    st.success(f"📟 Total: ₹{total}")

    # Payment method selection
    payment_method = st.selectbox("💳 Choose Payment Method", ["Credit Card", "Debit Card", "UPI", "Cash on Delivery"])

    if st.button("✅ Place Order"):
        order_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.success(f"🎉 Order placed at {order_time} using {payment_method}!")

        df_to_save = cart_df.copy()
        df_to_save["username"] = st.session_state.get("username")
        df_to_save["timestamp"] = order_time
        df_to_save["payment_method"] = payment_method

        # Save to CSV
        file_path = "data/purchase_history.csv"
        file_exists = os.path.exists(file_path)
        df_to_save.to_csv(file_path, mode='a', index=False, header=not file_exists)

        # Anomaly detection
        item_counts = df_to_save['name'].value_counts()
        for item, count in item_counts.items():
            if count >= 5:
                st.warning(f"⚠️ Anomaly Detected: {count} units of '{item}' in one order.")

        # Optional: Run fraud detection if schema matches
        try:
            required_columns = {'payment_method', 'login_location', 'device_type', 'browser_os',
                                'cookie_behavior', 'session_token_behavior', 'email_reputation'}

            if required_columns.issubset(df_to_save.columns):
                fraud_results = predict_fraud(df_to_save)
                st.info("Fraud detection run (demo mode).")
            else:
                st.info("Skipping fraud detection (missing required fields).")
        except Exception as e:
            st.error(f"Fraud check failed: {e}")

        st.session_state.cart = []

else:
    st.info("🛒 Your cart is empty.")

# ---------------------
# 📦 Show Past Orders
# ---------------------
st.header("📦 Your Past Orders")
try:
    df_history = pd.read_csv("data/purchase_history.csv")
    df_user_orders = df_history[df_history["username"] == st.session_state.get("username")]
    if not df_user_orders.empty:
        st.dataframe(df_user_orders.sort_values(by="timestamp", ascending=False))
    else:
        st.info("No past orders found.")
except FileNotFoundError:
    st.info("No order history available yet.")
