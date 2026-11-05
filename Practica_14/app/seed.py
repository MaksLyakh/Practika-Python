from datetime import date, time, timedelta
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_engine, init_db
from app.models.appointment import Appointment, User
from app.security import hash_password

DOCTORS = [("Иванов Иван Петрович", "Терапевт"), ("Смирнова Анна Сергеевна", "Кардиолог"),
           ("Петров Олег Викторович", "Невролог"), ("Кузнецова Мария Игоревна", "Хирург")]

def main():
    init_db()
    with sessionmaker(bind=get_engine(), expire_on_commit=False)() as db:
        admin = db.scalar(select(User).where(User.username == settings.admin_username))
        if admin is None:
            db.add(User(username=settings.admin_username, password_hash=hash_password(settings.admin_password), role="ADMIN"))
            db.commit()
            print("Создан ADMIN:", settings.admin_username)
        if db.scalar(select(Appointment.id).limit(1)) is None:
            for i in range(24):
                doctor, specialty = DOCTORS[i % 4]
                db.add(Appointment(patient=f"Пациент {i+1}", doctor=doctor, specialty=specialty,
                                   date=date(2026, 12, 10) + timedelta(days=i // 4),
                                   time=time(9 + i % 8, 0), room=100 + i % 4,
                                   status=["scheduled", "completed", "cancelled"][i % 3]))
            db.commit()
            print("Добавлено 24 приёма")
        else:
            print("Приёмы уже существуют, дублирование пропущено")

if __name__ == "__main__":
    main()
