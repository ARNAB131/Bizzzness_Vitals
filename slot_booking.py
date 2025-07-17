import uuid
from datetime import datetime, timedelta

def suggest_slots(existing_appointments, days=3):
    now = datetime.now()
    slots = []
    for d in range(days):
        date = now + timedelta(days=d)
        for hour in range(9, 17):  # 9 AM to 4 PM
            slot_time = datetime(date.year, date.month, date.day, hour)
            if slot_time.strftime("%Y-%m-%d %H:%M") not in existing_appointments:
                slots.append(slot_time.strftime("%Y-%m-%d %H:%M"))
    return slots[:5]

def book_slot(patient_id, slot_time):
    appointment_id = str(uuid.uuid4())[:8]
    return {"appointment_id": appointment_id, "patient_id": patient_id, "slot": slot_time}
