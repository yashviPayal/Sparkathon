import streamlit as st

st.set_page_config(
    page_title="🛒 E-Commerce Security Dashboard",
    layout="wide"
)

# -------------------------
# 🛡️ Session State Init
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# -------------------------
# 👤 Sidebar for Logged-in Users
# -------------------------
if st.session_state.logged_in:
    with st.sidebar:
        st.markdown(f"👤 Logged in as: **{st.session_state.username}** ({st.session_state.role})")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = ""
            st.success("🔓 You have been logged out.")
            st.experimental_rerun()

# -------------------------
# 🏠 Main View: Welcome
# -------------------------
st.title("🛍️ Welcome to the E-Commerce Security Dashboard")
st.markdown("Built with ❤️ to keep your online store safe from fraud, bots, and threats.")

st.divider()

if not st.session_state.logged_in:
    st.warning("🔐 You are not logged in.")
    st.markdown("Please **log in or register** to access your dashboard.")

    col1, col2 = st.columns(2)
    with col1:
        st.button("🔐 Login", use_container_width=True, on_click=lambda: st.switch_page("pages/2_Login.py"))

    with col2:
        st.button("📝 Register", use_container_width=True, on_click=lambda: st.switch_page("pages/3_Register.py"))


    st.markdown("---")
    st.markdown("🚨 Don’t have an account yet? Click **Register** to get started.")
else:
    st.success(f"✅ Welcome back, **{st.session_state.username}**!")
    st.markdown("Use the **sidebar** to access your **User** or **Admin** dashboard.")
