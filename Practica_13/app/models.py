from datetime import date, datetime
from uuid import uuid4

STATUSES = {"scheduled", "completed", "cancelled"}

def validate_appointment(data):
    required = ("patient", "doctor", "specialty", "date", "time", "diagnosis", "prescriptions", "status")
    if not isinstance(data, dict) or any(k not in data for k in required):
        raise ValueError("Не заполнены обязательные поля записи")
    for key in ("patient", "doctor"):
        if not isinstance(data[key], dict) or not data[key].get("id") or not data[key].get("name"):
            raise ValueError(f"{key}: требуются id и name")
    if not isinstance(data["prescriptions"], list):
        raise ValueError("prescriptions должен быть массивом")
    if data["status"] not in STATUSES:
        raise ValueError("Недопустимый статус")
    try:
        date.fromisoformat(data["date"])
        datetime.strptime(data["time"], "%H:%M")
    except (TypeError, ValueError) as exc:
        raise ValueError("Дата YYYY-MM-DD, время HH:MM") from exc
    if not isinstance(data["specialty"], str) or not data["specialty"].strip():
        raise ValueError("Укажите специальность")
    if not isinstance(data["diagnosis"], str):
        raise ValueError("Диагноз должен быть строкой")
    return data

def make_appointment(patient_id, patient_name, doctor_id, doctor_name,
                     specialty, day, time, diagnosis="", prescriptions=None,
                     status="scheduled", appointment_id=None):
    result = {
        "appointment_id": appointment_id or str(uuid4()),
        "patient": {"id": patient_id, "name": patient_name},
        "doctor": {"id": doctor_id, "name": doctor_name},
        "specialty": specialty, "date": day, "time": time,
        "diagnosis": diagnosis, "prescriptions": prescriptions or [],
        "status": status,
    }
    return validate_appointment(result)
