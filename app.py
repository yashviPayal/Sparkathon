import streamlit as st

st.set_page_config(
    page_title="E-Commerce Security Dashboard",
    layout="wide",
)

# 🛡️ Initialize session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# 🔘 LOGOUT UI in Sidebar
if st.session_state.logged_in:
    with st.sidebar:
        st.markdown(f"👤 Logged in as: **{st.session_state.username}** ({st.session_state.role})")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = ""
            st.success("🔓 You have been logged out. Redirecting to Login...")

            # 🔁 Redirect to login after short delay
            st.experimental_rerun()

# 🛒 Dashboard Title
st.title("🛒 E-Commerce Security Dashboard")
st.write("Welcome! Use the sidebar to access login, user panel, or admin panel.")
