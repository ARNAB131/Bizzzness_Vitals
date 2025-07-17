import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(page_title="Bizzzness Vitals Dashboard", layout="wide")

st.title("🏥 Bizzzness Vitals Monitoring Dashboard")

# ✅ Path to your compressed model
model_path = "models/model_compressed.pkl"

# ✅ Check if model exists
if not os.path.exists(model_path):
    st.error("❌ Model file not found! Please ensure model_compressed.pkl exists in models/")
    st.stop()
else:
    st.success("✅ Model Loaded Successfully!")
    model = joblib.load(model_path)

# ✅ Example interface after model loaded
st.header("Patient Vitals Predictor Example")

uploaded_file = st.file_uploader("Upload Patient Data CSV (optional):")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded Data:", df)

    if st.button("Predict"):
        prediction = model.predict(df)
        st.success("✅ Prediction Complete")
        st.write("Prediction Output:", prediction)

else:
    st.info("📄 Please upload a patient data CSV to predict.")

