from datetime import date, timedelta
from app.models import make_appointment
from app.db import connect

DOCTORS = [
    ("D01", "Иванов Иван Петрович", "Терапевт"),
    ("D02", "Смирнова Анна Сергеевна", "Кардиолог"),
    ("D03", "Петров Олег Викторович", "Невролог"),
    ("D04", "Кузнецова Мария Игоревна", "Хирург"),
]
PRESCRIPTIONS = [
    ["Общий анализ крови", "Повторный приём"],
    ["ЭКГ", "Контроль давления"],
    ["МРТ", "Консультация невролога"],
    ["Перевязка", "Повторный осмотр"],
]

def seed(repo, service, count=24):
    added = 0
    base = date(2026, 12, 10)
    for i in range(count):
        doctor_id, doctor_name, specialty = DOCTORS[i % len(DOCTORS)]
        day = (base + timedelta(days=i // 4)).isoformat()
        item = make_appointment(
            f"P{i+1:03}", f"Пациент {i+1}", doctor_id, doctor_name,
            specialty, day, f"{9 + i % 8:02}:00",
            ["ОРВИ", "Гипертония", "Мигрень", "Осмотр"][i % 4],
            PRESCRIPTIONS[i % 4], ["scheduled", "completed", "cancelled"][i % 3],
            appointment_id=f"A{i+1:03}",
        )
        if repo.get(item["appointment_id"]) is None:
            service.create_appointment(item)
            added += 1
    return added

def main():
    mongo, redis_client, service = connect()
    try:
        count = seed(service.repo, service)
        print(f"Добавлено записей: {count}; всего: {service.repo.collection.count_documents({})}")
    finally:
        mongo.close()
        redis_client.close()

if __name__ == "__main__":
    main()
