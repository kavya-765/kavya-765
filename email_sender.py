import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText

# Initialize session state to track email statistics
if "email_stats" not in st.session_state:
    st.session_state["email_stats"] = {"Sent": 0, "Delivered": 0, "Landed in Inbox": 0, "Landed in Spam": 0}

# Function to load recipients from CSV file
def load_recipients(csv_file):
    data = pd.read_csv(csv_file)
    return data['email'].tolist()

# Function to send emails in bulk and update statistics
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
                st.session_state["email_stats"]["Sent"] += 1
                st.session_state["email_stats"]["Delivered"] += 1  # Simplified; adjust as needed based on actual status
                st.write(f"Email sent to {email}")
            except Exception as e:
                st.session_state["email_stats"]["Landed in Spam"] += 1
                st.error(f"Failed to send email to {email}: {e}")

# Main email composing and scheduling functionality
def main_page():
    st.markdown("<h1 style='text-align: center;'>Email Composer</h1>", unsafe_allow_html=True)
    
    # Email input fields
    subject = st.text_input("Subject")
    body = st.text_area("Body", height=200)

    # CSV uploader for recipient emails
    csv_file = st.file_uploader("Upload CSV file with email addresses", type="csv")
    
    if st.button("Send Mass Emails") and csv_file:
        recipients = load_recipients(csv_file)
        sender_email = "kavyat7605@gmail.com"  # replace with actual email
        sender_password = "zxon whkm ssft ivnk"  # replace with actual password
        send_email(recipients, subject, body, sender_email, sender_password)
        st.success("Mass emails sent successfully!")
