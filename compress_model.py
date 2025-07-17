import joblib

# Load compressed model using joblib
model = joblib.load('models/model_compressed.pkl')

print("✅ Compressed model loaded successfully!")
