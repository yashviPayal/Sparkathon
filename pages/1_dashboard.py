import streamlit as st
import pandas as pd
import datetime
import os

# ----------------------------
# 🛡️ This is a honeypot bot dashboard
# ----------------------------
st.set_page_config(page_title="User Dashboard", layout="wide")
st.title("🛍️ User Dashboard")

if not st.session_state.get("logged_in") or st.session_state.get("role") != "bot":
    st.warning("⛔ Unauthorized access.")
    st.stop()

st.success(f"🤖 Welcome, {st.session_state.get('username')}")

st.markdown("""
> This is a real e-commerce shopping dashboard with dynamic data and interactive behavior logging.
""")

# Simulated products (identical to real one)
products = [
    {"name": "Wireless Headphones", "price": 1200},
    {"name": "Smartwatch", "price": 2499},
    {"name": "Bluetooth Speaker", "price": 999},
    {"name": "Phone Case", "price": 299},
    {"name": "Power Bank", "price": 699}
]

if "bot_cart" not in st.session_state:
    st.session_state.bot_cart = []

cols = st.columns(2)
for i, product in enumerate(products):
    with cols[i % 2]:
        st.subheader(product["name"])
        st.write(f"💰 Price: ₹{product['price']}")
        qty_key = f"qty_{product['name']}_bot"
        quantity = st.number_input(f"Quantity for {product['name']}", 1, 10, 1, key=qty_key)
        if st.button(f"Add to Cart: {product['name']}", key=product["name"] + "_bot"):
            st.session_state.bot_cart.append({
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity
            })

if st.session_state.bot_cart:
    st.subheader("🛒 Your Cart")
    cart_df = pd.DataFrame(st.session_state.bot_cart)
    cart_df["total"] = cart_df["price"] * cart_df["quantity"]
    st.dataframe(cart_df)

    total = cart_df["total"].sum()
    st.success(f"📿 Total: ₹{total}")

    if st.button("✅ Fake Checkout (Logged)"):
        order_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Simulate behavior metrics (this could be extracted from JS or backend monitoring)
        fake_bot_behavior = {
            "username": st.session_state["username"],
            "timestamp": order_time,
            "typing_time": 0.1,
            "click_count": 150,
            "scroll_depth": 100,
            "mouse_moves_per_second": 30,
            "hover_time": 1.0,
            "idle_time_ratio": 0.0,
            "keystroke_variance": 0.001,
            "mouse_click_rate": 10,
            "total_time_on_page": 20,
            "suspicious_cart_value": total
        }

        log_file = "data/bot_activity_log.csv"
        df_log = pd.DataFrame([fake_bot_behavior])
        if os.path.exists(log_file):
            old = pd.read_csv(log_file)
            df_log = pd.concat([old, df_log], ignore_index=True)

        df_log.to_csv(log_file, index=False)
        st.warning("🧠 Bot activity logged.")
        st.success("Thank you for your purchase!")
        st.session_state.bot_cart = []

else:
    st.info("🛒 Your cart is empty.")

