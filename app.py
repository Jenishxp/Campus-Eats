import streamlit as st
from auth.login import login
from auth.signup import signup
from user.dashboard import user_dashboard
from user.orders import user_orders
from vendor.dashboard import vendor_dashboard
from admin.dashboard import admin_dashboard

st.set_page_config(page_title="Campus Eats", layout="centered")

# ---------------- AUTH CHECK ----------------
if "user" not in st.session_state:
    tab1, tab2 = st.tabs(["Login", "Signup"])
    with tab1:
        login()
    with tab2:
        signup()

else:
    # ✅ DEFINE USER HERE
    user = st.session_state.user

    # ---------------- ROLE BASED UI ----------------
    if user["role"] == "user":
        tab1, tab2 = st.tabs(["🍽️ Order Food", "📦 My Orders"])
        with tab1:
            user_dashboard(user)
        with tab2:
            user_orders(user)

    elif user["role"] == "vendor":
        vendor_dashboard(user)

    elif user["role"] == "admin":
        admin_dashboard(user)

    # ---------------- LOGOUT ----------------
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun()
