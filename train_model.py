import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
import os

DATA_PATH = "data/vitals.csv"
MODEL_PATH = "models/model.pkl"

# ✅ Check file exists
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"❌ Vitals CSV not found at {DATA_PATH}")

# ✅ Load data
df = pd.read_csv(DATA_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.dropna(subset=["timestamp"])
df = df.sort_values("timestamp")

# ✅ Check enough data
if len(df) < 2:
    raise ValueError("❌ Not enough data to train. Need at least 2 records.")

# ✅ Define X and y
X = df[["heart_rate", "bp_systolic", "bp_diastolic", "oxygen_saturation", "temperature"]][:-1]
y = df[["heart_rate", "bp_systolic", "bp_diastolic", "oxygen_saturation", "temperature"]].shift(-1).dropna()

# ✅ Train model
model = MultiOutputRegressor(RandomForestRegressor())
model.fit(X, y)

# ✅ Save model
os.makedirs("models", exist_ok=True)
with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved to models/model.pkl")
