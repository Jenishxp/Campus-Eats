import streamlit as st
from auth.auth_service import signup_user

def signup():
    st.subheader("Signup")

    name = st.text_input("Name", key="signup_name")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    role = st.selectbox("Role", ["user", "vendor"], key="signup_role")

    shop_name = None
    if role == "vendor":
        shop_name = st.text_input("Shop Name", key="signup_shop")

    if st.button("Create Account", key="signup_btn"):
        signup_user(name, email, password, role, shop_name)
        st.success("Account created successfully!")
