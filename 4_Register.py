#4_Register.py
import streamlit as st
from utils.auth import save_user

st.title("📝 Register")

new_username = st.text_input("Choose a username")
new_password = st.text_input("Choose a password", type="password")
register_button = st.button("Register")

if register_button:
    if not new_username or not new_password:
        st.error("Please enter both username and password.")
    elif len(new_password) < 6:
        st.error("Password should be at least 6 characters long.")
    else:
        success = save_user(new_username, new_password)
        if success:
            st.success("Account created. You can now log in.")
        else:
            st.error("Username already exists.")
