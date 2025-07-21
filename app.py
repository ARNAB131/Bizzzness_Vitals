import streamlit as st
import pandas as pd
import joblib
import os
import time
from slot_booking import suggest_slots, book_slot
from text_to_speech import speak
from utils.email_alert import send_email_alert

st.set_page_config(page_title="Bizzzness Vitals Dashboard", layout="wide")

st.markdown("<h1 style='text-align:center; color:#4CAF50;'>🏥 Bizzzness Vitals Monitoring Dashboard</h1>", unsafe_allow_html=True)

# ✅ Model Load
model_path = "models/model_compressed.pkl"
VALID_FEATURES = ['heart_rate', 'bp_systolic', 'bp_diastolic', 'oxygen_saturation', 'temperature']

if not os.path.exists(model_path):
    st.error("❌ Model file not found!")
    st.stop()
else:
    model = joblib.load(model_path)

# ✅ Tab Layout
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📄 Vitals Prediction", "📅 Slot Booking", "🗣️ Text to Speech", "📧 Email Alerts", "📥 Downloads"])

# ✅ 📄 Tab 1: Vitals Prediction
with tab1:
    st.header("📄 Patient Vitals Predictor")
    uploaded_file = st.file_uploader("📁 Upload Patient Data (CSV or Excel)", type=["csv", "xlsx"])
    if uploaded_file:
        filename = uploaded_file.name
        try:
            if filename.endswith(".csv"):
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            elif filename.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                st.error("❌ Unsupported file format!")
                st.stop()
            st.dataframe(df)
            missing = [col for col in VALID_FEATURES if col not in df.columns]
            if missing:
                st.error(f"❌ Missing columns: {missing}")
                st.stop()
            df_filtered = df[VALID_FEATURES]
            if st.button("🔮 Predict"):
                prediction = model.predict(df_filtered)
                st.success("✅ Prediction Done!")
                st.write(prediction)
                st.toast("✅ Prediction Completed", icon="🔮")
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")
    else:
        st.info("📁 Upload patient data file to predict.")

# ✅ 📅 Tab 2: Slot Booking
with tab2:
    st.header("📅 Slot Booking System")
    patient_id = st.text_input("Enter Patient ID (required to book):")
    existing_appointments = []
    if patient_id:
        slots = suggest_slots(existing_appointments)
        chosen_slot = st.selectbox("Choose your slot:", slots)
        if st.button("✅ Book Slot"):
            booking = book_slot(patient_id, chosen_slot)
            st.success(f"✅ Slot booked with ID: {booking['appointment_id']} at {booking['slot']}")
            speak(f"Slot booked for {patient_id} at {booking['slot']}")
            st.toast("✅ Slot booked successfully!", icon="📅")
    else:
        st.warning("⚠️ Enter Patient ID to enable booking.")

# ✅ 🗣️ Tab 3: Text to Speech
with tab3:
    st.header("🗣️ Text to Speech")
    tts_text = st.text_input("Say something:")
    if st.button("🗣️ Speak Now"):
        speak(tts_text)
        st.success("✅ Spoken (locally), printed in console on Render.")
        st.toast("✅ Text spoken", icon="🗣️")

# ✅ 📧 Tab 4: Email Alerts
with tab4:
    st.header("📧 Send Email Alert (via Patient Gmail App Password)")
    patient_gmail = st.text_input("Enter Patient Gmail (Sender):")
    patient_app_password = st.text_input("Enter App Password:", type="password")
    doctor_email = st.text_input("Enter Doctor Email:")
    subject = st.text_input("Enter Email Subject:")
    message = st.text_area("Enter Email Message:")
    if st.button("🚨 Send Email"):
        if all([patient_gmail, patient_app_password, doctor_email, subject, message]):
            result = send_email_alert(patient_gmail, patient_app_password, doctor_email, subject, message)
            if result:
                st.success("✅ Email sent successfully!")
                st.toast("✅ Email Sent", icon="📧")
            else:
                st.error("❌ Failed to send email!")
        else:
            st.warning("⚠️ Fill in all fields before sending email.")

# ✅ 📥 Tab 5: Downloads
with tab5:
    st.header("📥 Download Example Data")
    example_data = pd.DataFrame({
        'heart_rate': [70, 80],
        'bp_systolic': [120, 130],
        'bp_diastolic': [80, 85],
        'oxygen_saturation': [98.5, 97.2],
        'temperature': [36.7, 37.1]
    })
    st.download_button("📥 Download CSV Template", data=example_data.to_csv(index=False), file_name="vitals_template.csv")
    st.success("✅ Download Sample Template for Testing")

    st.header("📊 Live Simulated Data (10 seconds)")
    placeholder = st.empty()
    for _ in range(10):
        simulated = pd.read_csv('data/vitals.csv').sample(5)
        placeholder.dataframe(simulated)
        time.sleep(1)
