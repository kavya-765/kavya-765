import streamlit as st
from db import get_session, users
from add_user import add_user  # Import the add_user function

# Initialize session for database
session = get_session()

# Function to authenticate users
def authenticate_user(username, password):
    user = session.query(users).filter_by(username=username, password=password).first()
    return user is not None

# Initialize session state variables
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "register_mode" not in st.session_state:
    st.session_state["register_mode"] = False

# Function to render the login page
def login_page():
    st.markdown("""
        <style>
            .login-container {
                max-width: 400px;
                margin: auto;
                padding: 2rem;
                border: 1px solid #ddd;
                border-radius: 10px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            .login-title {
                font-size: 2rem;
                font-weight: bold;
                margin-bottom: 0.5rem;
            }
            .login-subtitle {
                font-size: 1rem;
                color: #888;
                margin-bottom: 1.5rem;
            }
            .stButton>button {
                background-color: black;
                color: white;
                padding: 1rem 2rem;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 1rem;
            }
            .register-link {
                margin-top: 1rem;
                font-size: 0.9rem;
                color: #007bff;
                cursor: pointer;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown("<div class='login-title'>Welcome!</div>", unsafe_allow_html=True)
    st.markdown("<div class='login-subtitle'>Sign in to<br>Lorem Ipsum is simply</div>", unsafe_allow_html=True)

    username = st.text_input("User  name", placeholder="Enter your user name", key="login_username_key")
    password = st.text_input("Password", type="password", placeholder="Enter your Password", key="login_password_key")

    login_button = st.button("Login", key="login_button_key")

    if st.button("Don’t have an Account? Register", key="register_button_key"):
        st.session_state["register_mode"] = True

    if login_button:
        if authenticate_user(username, password):
            st.session_state["authenticated"] = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password.")

# Function to render the registration page
def register_page():
    st.markdown("<h2 style='text-align: center;'>Register</h2>", unsafe_allow_html=True)

    username = st.text_input("Choose a username", key="register_username_key")
    password = st.text_input("Choose a password", type="password", key="register_password_key")
    confirm_password = st.text_input("Confirm password", type="password", key="register_confirm_password_key")

    if st.button("Register", key="register_submit_button_key"):
        if password != confirm_password:
            st.error("Passwords do not match. Please try again.")
        elif add_user(username, password):
            st.success("Registration successful! Please log in now.")
            st.session_state["register_mode"] = False
        else:
            st.error("Username already exists. Please choose a different username.")

# Main Application Logic
if not st.session_state["authenticated"]:
    if st.session_state["register_mode"]:
        register_page()
    else:
        login_page()
else:
    st.write("You are logged in! You can now access other parts of the application.")
