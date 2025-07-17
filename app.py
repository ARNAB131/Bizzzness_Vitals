# Main Streamlit dashboard (AI edition)
print('Streamlit App Loaded')
import streamlit as st
import pandas as pd
import pickle
import os
import time
import matplotlib.pyplot as plt

from utils.email_alert import send_email_alert
from slot_booking import suggest_slots, book_slot
from text_to_speech import speak

# --- Paths ---
DATA_PATH = "data/vitals.csv"
MODEL_PATH = "models/model.pkl"

# --- Load Model ---
if not os.path.exists(MODEL_PATH):
    st.error("Model file not found!")
    st.stop()

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# --- Load Data ---
if not os.path.exists(DATA_PATH):
    st.error("Vitals CSV file not found!")
    st.stop()

df = pd.read_csv(DATA_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.dropna(subset=["timestamp"])
df = df.sort_values("timestamp", ascending=False)
# --- Email Configuration (Sidebar) ---
st.sidebar.subheader("📧 Email Configuration")

patient_gmail = st.sidebar.text_input("Patient Gmail (sender)", placeholder="example@gmail.com")
patient_app_password = st.sidebar.text_input("App Password", type="password")
doctor_gmail = st.sidebar.text_input("Doctor Gmail (receiver)", placeholder="doctor@gmail.com")


# --- UI ---
st.title("🩺 Bizzzness Vitals Monitoring + AI Co-Pilot")

patient_ids = sorted(df["patient_id"].unique())
selected_patient = st.selectbox("Select Patient ID", patient_ids)

patient_data = df[df["patient_id"] == selected_patient]
if patient_data.empty:
    st.warning("No data available for this patient.")
    st.stop()

latest = patient_data.iloc[0]

st.subheader("📊 Latest Vitals")
vitals_display = {
    "🫀 Heart Rate": int(latest["heart_rate"]),
    "🔼 Systolic BP": int(latest["bp_systolic"]),
    "🔽 Diastolic BP": int(latest["bp_diastolic"]),
    "🩸 SpO2": int(latest["oxygen_saturation"]),
    "🌡️ Temperature": round(float(latest["temperature"]), 1),
    "⏱️ Timestamp": latest["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
}
st.write(vitals_display)

# ✅ Speech Toggle
enable_speech = st.checkbox("🔈 Enable Text-to-Speech", value=True)

if enable_speech:
    speak("Here are the latest vitals")
    for k, v in vitals_display.items():
        speak(f"{k}: {v}")


# Text-to-speech
if st.button("🔊 Read Aloud"):
    speak("Here are the latest vitals")
    for k, v in vitals_display.items():
        speak(f"{k}: {v}")

# --- Predictions ---
input_df = pd.DataFrame([latest[["heart_rate", "bp_systolic", "bp_diastolic", "oxygen_saturation", "temperature"]]])
predicted = model.predict(input_df)[0]

st.subheader("🔮 Predicted Next Vitals")
labels = ["Heart Rate", "Systolic BP", "Diastolic BP", "Oxygen Saturation", "Temperature"]
for label, value in zip(labels, predicted):
    st.write(f"{label}: {value:.2f}")

# --- Vitals History ---
st.subheader("📈 Vitals History")
fig, ax = plt.subplots(figsize=(10, 5))
for vital in ["heart_rate", "bp_systolic", "bp_diastolic", "oxygen_saturation", "temperature"]:
    ax.plot(patient_data["timestamp"], patient_data[vital], label=vital)
ax.legend()
ax.set_xlabel("Time")
ax.set_ylabel("Values")
plt.xticks(rotation=45)
st.pyplot(fig)

# --- Alert ---
thresholds = {
    "heart_rate": 100,
    "bp_systolic": 140,
    "bp_diastolic": 90,
    "oxygen_saturation": 92,
    "temperature": 38.0
}
alerts = []
for i, label in enumerate(labels):
    key = label.lower().replace(" ", "_")
    if predicted[i] > thresholds[key]:
        alerts.append(f"{label}: {predicted[i]:.2f}")

if alerts:
    msg = f"🚨 Critical vitals for patient {selected_patient}:\n\n" + "\n".join(alerts)

    if patient_gmail and patient_app_password and doctor_gmail:
        success = send_email_alert(
            patient_gmail=patient_gmail,
            patient_app_password=patient_app_password,
            doctor_gmail=doctor_gmail,
            subject="🚨 Vitals Alert",
            message=msg
        )
        if success:
            st.success("📩 Alert sent to doctor successfully.")
        else:
            st.error("⚠️ Failed to send alert. Check Gmail or App Password.")
    else:
        st.warning("🔐 Please enter patient Gmail, App Password, and doctor Gmail to send alerts.")


# --- Book Slot ---
from slot_booking import suggest_slots, book_slot

# Dummy: Replace with your stored appointment list later
existing_appointments = []  # e.g., ['2025-07-12 10:00', '2025-07-12 14:00']

st.subheader("📅 Available Doctor Slots")
available_slots = suggest_slots(existing_appointments)

selected_slot = st.selectbox("Choose a slot to book", available_slots)

if st.button("✅ Confirm Slot Booking"):
    booking = book_slot(selected_patient, selected_slot)
    success_msg = f"✅ Appointment booked!\n\n🆔 ID: {booking['appointment_id']}\n👤 Patient ID: {booking['patient_id']}\n🕒 Slot: {booking['slot']}"
    st.success(success_msg)
    speak("Slot booked successfully for Patient")
    speak(success_msg)

st.caption("⏱️ Auto-refreshing every 10 seconds...")
time.sleep(10)
st.rerun()
