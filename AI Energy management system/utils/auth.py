# auth.py
import streamlit as st

users = {
    "sravani": {"password": "1234", "name": "Sravani"},
    "admin": {"password": "admin", "name": "Administrator"},
    "newuser": {"password": "newpass", "name": "New User"}  # You can add this
}

def login_user(username, password):
    user = users.get(username)
    if user and user["password"] == password:
        return user
    return None

