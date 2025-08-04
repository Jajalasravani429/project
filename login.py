# login.py
import streamlit as st
from utils.auth import login_user

def show_login():
    st.title("🔐 User Login")
    st.markdown("Please login to access your personalized energy dashboard.")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            user = login_user(username, password)
            if user:
                st.session_state["logged_in"] = True
                st.session_state["user"] = {
                    "username": username,
                    "name": user["name"]
                }
                st.success(f"Welcome, {user['name']}!")
                st.rerun()

            else:
                st.error("Invalid username or password")
