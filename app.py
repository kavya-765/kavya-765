import streamlit as st
from login import login_page
from email_sender import main_page

# Initialize 'authenticated' session state if it doesn't exist
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Define the logout function
def logout():
    st.session_state["authenticated"] = False
    st.sidebar.success("You have been logged out.")
    login_page()  # Redirect to login page immediately
    st.stop()  # Stops further execution

# Define app structure
def app():
    # Display the login page if the user is not authenticated
    if not st.session_state["authenticated"]:
        login_page()  # Import and call login page from login.py

    # Once authenticated, show the main page (email sender functionality)
    else:
        st.sidebar.title("Navigation")
        page_selection = st.sidebar.radio("Go to", ["Email Composer", "Logout"])

        if page_selection == "Email Composer":
            main_page()  # Import and call main page from email_sender.py

        elif page_selection == "Logout":
            logout()  # Call the logout function

if __name__ == "__main__":
    app()
