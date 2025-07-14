import streamlit as st
from utils.auth import verify_login

st.set_page_config(page_title="Login", layout="centered")
st.title("🔐 Login")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.phone = ""
    st.session_state.email = ""

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    user_data = verify_login(username, password)
    if user_data:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.role = user_data["role"]
        st.session_state.phone = user_data.get("phone", "")
        st.session_state.email = user_data.get("email", "")
        st.success(f"✅ Welcome, {username}! You are logged in as **{user_data['role']}**.")

        # Redirect based on role
        if user_data["role"] == "admin":
            st.switch_page("pages/5_Admin_Dashboard.py")
        elif user_data["role"] == "user":
            st.switch_page("pages/4_User_Dashboard.py")
        elif user_data["role"] == "bot":
            st.warning("🤖 Bot detected — redirecting to honeypot.")
            st.switch_page("pages/1_dashboard.py")  # You may rename this to bot_dashboard.py
        else:
            st.error("🚫 Unknown role. Contact support.")

    else:
        st.error("❌ Invalid username or password.")
