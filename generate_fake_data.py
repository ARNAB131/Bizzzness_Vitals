import pandas as pd
import random
from datetime import datetime, timedelta

NUM_PATIENTS = 5
RECORDS_PER_PATIENT = 3
OUTPUT_FILE = "data/vitals.csv"

data = []

for patient_id in range(1, NUM_PATIENTS + 1):
    timestamp = datetime.now() - timedelta(days=RECORDS_PER_PATIENT)
    for _ in range(RECORDS_PER_PATIENT):
        timestamp += timedelta(minutes=random.randint(5, 60))
        record = {
            "patient_id": patient_id,
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "heart_rate": random.randint(70, 110),
            "bp_systolic": random.randint(110, 160),
            "bp_diastolic": random.randint(70, 100),
            "oxygen_saturation": random.randint(90, 100),
            "temperature": round(random.uniform(36.0, 38.5), 1)
        }
        data.append(record)

df = pd.DataFrame(data)
df.to_csv(OUTPUT_FILE, index=False)

print(f"✅ Generated {len(data)} records for {NUM_PATIENTS} patients in {OUTPUT_FILE}")
