import streamlit as st
import pandas as pd
import joblib
import os
from slot_booking import suggest_slots, book_slot
from text_to_speech import speak
from utils.email_alert import send_email_alert  # ✅ Added for email alerts

st.set_page_config(page_title="Bizzzness Vitals Dashboard", layout="wide")

st.title("🏥 Bizzzness Vitals Monitoring Dashboard")

# ✅ Model Load Section
model_path = "models/model_compressed.pkl"

if not os.path.exists(model_path):
    st.error("❌ Model file not found! Please ensure model_compressed.pkl exists in models/")
    st.stop()
else:
    st.success("✅ Model Loaded Successfully!")
    model = joblib.load(model_path)

VALID_FEATURES = ['heart_rate', 'bp_systolic', 'bp_diastolic', 'oxygen_saturation', 'temperature']

# ✅ 📅 SLOT BOOKING SECTION
st.header("📅 Slot Booking System")

patient_id = st.text_input("Enter Patient ID (required to book):")
existing_appointments = []  # Future: Replace with database list

if patient_id:
    slots = suggest_slots(existing_appointments)
    chosen_slot = st.selectbox("Choose your slot:", slots)

    if st.button("✅ Book Slot"):
        booking = book_slot(patient_id, chosen_slot)
        st.success(f"✅ Slot booked with Appointment ID: {booking['appointment_id']}")
        st.info(f"⏰ Time: {booking['slot']}")
        speak(f"Slot booked for patient {patient_id} at {booking['slot']}")
else:
    st.warning("⚠️ Enter Patient ID to enable booking.")

# ✅ 🗣️ TEXT-TO-SPEECH SECTION
st.header("🗣️ Text-to-Speech (Local/Console)")
tts_text = st.text_input("Say something:")

if st.button("🗣️ Speak Now"):
    speak(tts_text)
    st.success("✅ Text spoken (locally), printed on Render.")

# ✅ 📄 VITALS PREDICTION SECTION
st.header("📄 Patient Vitals Predictor")

uploaded_file = st.file_uploader("📁 Upload Patient Data (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    filename = uploaded_file.name
    try:
        if filename.endswith(".csv"):
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("❌ Unsupported file format!")
            st.stop()

        st.success("✅ File uploaded successfully!")
        st.dataframe(df)

        missing = [col for col in VALID_FEATURES if col not in df.columns]
        if missing:
            st.error(f"❌ Missing columns: {missing}")
            st.stop()

        df_filtered = df[VALID_FEATURES]
        st.info("✅ Data ready for prediction.")
        st.dataframe(df_filtered)

        if st.button("🔮 Predict"):
            try:
                prediction = model.predict(df_filtered)
                st.success("✅ Prediction Done!")
                st.write("📊 Prediction Output:", prediction)
            except Exception as e:
                st.error(f"❌ Prediction Error: {e}")
    except Exception as e:
        st.error(f"❌ File reading error: {e}")
else:
    st.info("📁 Upload patient data file to predict.")

# ✅ 📧 EMAIL ALERT SECTION
st.header("📧 Send Email Alert")

patient_gmail = st.text_input("Enter Patient Gmail (Sender):")
patient_app_password = st.text_input("Enter Patient App Password (Sender Password):", type="password")
doctor_email = st.text_input("Enter Doctor's Email (Recipient):")
subject = st.text_input("Enter Email Subject:")
message = st.text_area("Enter Message (Symptoms, Notes, etc.):")

if st.button("🚨 Send Email Alert"):
    if patient_gmail and patient_app_password and doctor_email and subject and message:
        try:
            success = send_email_alert(patient_gmail, patient_app_password, doctor_email, subject, message)
            if success:
                st.success("✅ Email alert sent successfully!")
            else:
                st.error("❌ Failed to send email. Please check your credentials or recipient address.")
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")
    else:
        st.warning("⚠️ Please fill in all fields.")
