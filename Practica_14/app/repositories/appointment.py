from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session
from app.models.appointment import Appointment

SORT_FIELDS = {"id", "patient", "doctor", "specialty", "date", "time", "room", "status"}

class AppointmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, appointment_id: int):
        return self.db.get(Appointment, appointment_id)

    def list(self, *, limit=20, offset=0, sort="date", order="asc", specialty=None, status=None, doctor=None, q=None):
        stmt = select(Appointment)
        if specialty:
            stmt = stmt.where(Appointment.specialty == specialty)
        if status:
            stmt = stmt.where(Appointment.status == status)
        if doctor:
            stmt = stmt.where(Appointment.doctor.ilike(f"%{doctor}%"))
        if q:
            stmt = stmt.where(Appointment.patient.ilike(f"%{q}%") | Appointment.doctor.ilike(f"%{q}%"))
        total = self.db.scalar(select(func.count()).select_from(stmt.subquery()))
        column = getattr(Appointment, sort)
        stmt = stmt.order_by(desc(column) if order == "desc" else asc(column), Appointment.id).offset(offset).limit(limit)
        return total, list(self.db.scalars(stmt).all())

    def create(self, data: dict):
        obj = Appointment(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: Appointment, data: dict):
        for key, value in data.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: Appointment):
        self.db.delete(obj)
        self.db.commit()

    def statistics(self):
        rows = dict(self.db.execute(select(Appointment.status, func.count()).group_by(Appointment.status)).all())
        return {"total": sum(rows.values()), "scheduled": rows.get("scheduled", 0),
                "completed": rows.get("completed", 0), "cancelled": rows.get("cancelled", 0),
                "specialties": self.db.scalar(select(func.count(func.distinct(Appointment.specialty)))) or 0}
