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
st.header("📄 Patient Vitals Predictor")

uploaded_file = st.file_uploader("📁 Upload Patient Data CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # ✅ First try UTF-8
        df = pd.read_csv(uploaded_file, encoding='utf-8')
    except UnicodeDecodeError:
        # ✅ Fallback to Windows-safe encoding
        df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')

    st.success("✅ File uploaded and read successfully!")
    st.dataframe(df)

    if st.button("🔮 Predict"):
        try:
            prediction = model.predict(df)
            st.success("✅ Prediction Complete!")
            st.write("Prediction Output:", prediction)
        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")

else:
    st.info("📄 Please upload a patient data CSV to start predictions.")
