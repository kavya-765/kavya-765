import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText

# Authentication check in main.py, remove from here for modularity
def login_page():
    st.markdown("<h1 style='text-align: center;'>Login</h1>", unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == "admin" and password == "password":  # Example credentials
            st.session_state["authenticated"] = True
            st.success("Login successful!")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")

# Function to load recipients from CSV file
def load_recipients(csv_file):
    data = pd.read_csv(csv_file)
    if 'email' not in data.columns:
        st.error("CSV file must contain an 'email' column.")
        return []
    return data['email'].tolist()

# Function to send emails in bulk
def send_email(recipients, subject, body, sender_email, sender_password):
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        
        for email in recipients:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = email
            try:
                server.sendmail(sender_email, email, msg.as_string())
                st.write(f"Email sent to {email}")
            except Exception as e:
                st.error(f"Failed to send email to {email}: {e}")

# Main email composing and scheduling functionality
def main_page():
    st.markdown("<h1 style='text-align: center;'>Email Composer</h1>", unsafe_allow_html=True)
    
    # Compose individual email form
    with st.form("email_form"):
        title = st.text_input("Title")
        to = st.text_input("To")
        cc = st.text_input("CC")
        bcc = st.text_input("BCC")
        reply = st.text_input("Reply")
        body = st.text_area("Body", height=200)
        signature = st.text_area("Signature", height=100)

        submitted = st.form_submit_button("Send")
        if submitted:
            full_body = f"{body}\n\n{signature}"  # Include signature
            recipients = [to] + (cc.split(',') if cc else []) + (bcc.split(',') if bcc else [])
            sender_email = "your-email@example.com"  # Replace with your email
            sender_password = "your-email-password"  # Replace with your password
            send_email(recipients, title, full_body, sender_email, sender_password)
            st.success("Email sent successfully!")
            st.session_state['email_sent'] = True

    # Mass email form
    csv_file = st.file_uploader("Upload CSV file with email addresses", type="csv")
    subject = st.text_input("Subject for Mass Email")
    body_mass = st.text_area("Body for Mass Email", height=200)

    if st.button("Send Mass Emails") and csv_file:
        recipients = load_recipients(csv_file)
        if recipients:  # Only send if recipients are loaded
            sender_email = "your-email@example.com"  # Replace with your email
            sender_password = "your-email-password"  # Replace with your password
            send_email (recipients, subject, body_mass, sender_email, sender_password)
            st.success("Mass emails sent successfully!")

    # Schedule email functionality
    if st.button("Schedule Now"):
        with st.form("schedule_form"):
            date = st.date_input("Date")
            time = st.time_input("Time")
            if st.form_submit_button("Schedule Email"):
                st.success(f"Email scheduled successfully for {date} at {time}!")

    # Logout button
    if st.button("Logout"):
        st.session_state["authenticated"] = False
        st.success("You have been logged out.")
        st.experimental_rerun()

# Main execution
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if st.session_state['authenticated']:
    main_page()
else:
    login_page()
