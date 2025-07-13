import streamlit as st

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("📊 Welcome to the E-commerce Security Dashboard")

# -------------------------
# 🔐 Access Control
# -------------------------
if not st.session_state.get("logged_in"):
    st.warning("🔒 Please log in to access the dashboard.")
    st.stop()

username = st.session_state.get("username")
role = st.session_state.get("role")

st.success(f"✅ Logged in as: {username} ({role.capitalize()})")

# -------------------------
# 📚 Sidebar Role Menu
# -------------------------
with st.sidebar:
    st.header("🧭 Navigation")

    if role == "admin":
        st.page_link("pages/2_AdminPanel.py", label="🛠️ Admin Dashboard")
    elif role == "user":
        st.page_link("pages/3_UserPanel.py", label="👤 User Dashboard")

    st.divider()
    if st.button("🔓 Logout"):
        st.session_state.clear()
        st.success("Logged out successfully.")
        st.experimental_rerun()
