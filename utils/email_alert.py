import smtplib
from email.mime.text import MIMEText

def send_email_alert(patient_gmail, patient_app_password, doctor_gmail, subject, message):
    """
    Send an email from patient_gmail to doctor_gmail with subject and message.
    """
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = patient_gmail
    msg["To"] = doctor_gmail

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(patient_gmail, patient_app_password)
        server.sendmail(patient_gmail, doctor_gmail, msg.as_string())
        server.quit()
        print(f"✅ Email sent successfully from {patient_gmail} to {doctor_gmail}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False
