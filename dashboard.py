import streamlit as st
import pandas as pd

# Define a function to display the dashboard, pulling stats from session state
def dashboard_page():
    st.title("Email Campaign Dashboard")

    # Performance Summary using updated stats from session state
    st.subheader("Performance Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Sent", st.session_state["email_stats"]["Sent"])
    col2.metric("Delivered", st.session_state["email_stats"]["Delivered"])
    col3.metric("Landed in Inbox", st.session_state["email_stats"]["Landed in Inbox"])
    col4.metric("Landed in Spam", st.session_state["email_stats"]["Landed in Spam"])

    # Mailbox Management (example data, replace with dynamic mailbox data if available)
    st.subheader("Mailbox Management")
    mailbox_data = [
        {"Status": "Enabled", "Email": "user1@example.com", "Account Health": 8.0, "Deliverability": "82%", "Not Blacklisted": True},
        {"Status": "Enabled", "Email": "user2@example.com", "Account Health": 9.2, "Deliverability": "70%", "Not Blacklisted": True}
    ]
    mailbox_df = pd.DataFrame(mailbox_data)
    st.table(mailbox_df)

    # Deliverability Score
    st.subheader("Deliverability Score")
    score = 94  # Example static score; update based on email statistics if applicable
    st.progress(score / 100)
    st.write("Deliverability Score:", f"{score}%")

# Integrate with the main app
if __name__ == "__main__":
    if st.session_state.get("authenticated", False):
        dashboard_page()
    else:
        st.write("Please log in to view the dashboard.")
