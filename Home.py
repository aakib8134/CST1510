import streamlit as st

from app_model.users import add_user
from hashing import hash_password
from login import get_user, check_password, login_user
from app_model.db import check_connection

conn = check_connection()

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

st.title("Welcome to the Main Page 🏠")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False


tab_login, tab_register = st.tabs(["Login", "Register"])

with tab_login:
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input(
        "Password", type="password", key="login_password")

    if st.button("Log In"):
        username, password_hash = get_user(conn, login_username)
        if username == login_username and check_password(login_password, password_hash):
            st.session_state["logged_in"] = True
            st.success("Login successful! Welcome, " + username + "!")
            st.switch_page("pages/1_dashboard.py")
        else:
            st.session_state["logged_in"] = False


with tab_register:
    register_username = st.text_input("New Username")
    register_password = st.text_input("New Password", type="password")
    h_password = hash_password(register_password)
    if st.button("Register"):
        st.session_state["logged_in"] = False

        add_user(conn, register_username, h_password, "user")
        st.success("Registration successful! Please log in.")
