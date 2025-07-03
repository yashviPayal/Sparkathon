import streamlit as st
from utils.auth import verify_login

st.title("🔐 Login")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    role = verify_login(username, password)
    if role:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.role = role
        st.success(f"Welcome, {username}! You are logged in as {role}.")
    else:
        st.error("❌ Invalid username or password.")
