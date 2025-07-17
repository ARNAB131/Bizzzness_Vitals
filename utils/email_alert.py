import smtplib
from email.mime.text import MIMEText

def send_email_alert(patient_gmail, patient_app_password, doctor_gmail, subject, message):
    # Compose message
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
        print("✅ Email sent successfully.")
        return True
    except Exception as e:
        print("❌ Failed to send email:", e)
        return False
