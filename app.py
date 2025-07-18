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

# ✅ Define the expected feature columns used during model training
VALID_FEATURES = ['heart_rate', 'bp_systolic', 'bp_diastolic', 'oxygen_saturation', 'temperature']  # replace with your actual features

st.header("📄 Patient Vitals Predictor")

uploaded_file = st.file_uploader("📁 Upload Patient Data (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    filename = uploaded_file.name
    try:
        # ✅ Handle both CSV and Excel
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

        # ✅ Filter valid columns
        missing_cols = [col for col in VALID_FEATURES if col not in df.columns]
        if missing_cols:
            st.error(f"❌ Missing required columns: {missing_cols}")
            st.stop()

        df_filtered = df[VALID_FEATURES]
        st.info("✅ Data filtered and ready for prediction.")
        st.dataframe(df_filtered)

        if st.button("🔮 Predict"):
            try:
                prediction = model.predict(df_filtered)
                st.success("✅ Prediction Complete!")
                st.write("Prediction Output:", prediction)
            except Exception as e:
                st.error(f"❌ Prediction failed: {e}")
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
else:
    st.info("📄 Please upload a patient data CSV or Excel file to start predictions.")
