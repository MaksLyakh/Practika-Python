from fastapi import HTTPException
from app.repositories.appointment import AppointmentRepository
from app.schemas.appointment import AppointmentResponse

class AppointmentService:
    def __init__(self, repo: AppointmentRepository, cache):
        self.repo = repo
        self.cache = cache

    def get(self, appointment_id: int):
        cached = self.cache.get(appointment_id)
        if cached is not None:
            return cached
        obj = self.repo.get(appointment_id)
        if obj is None:
            raise HTTPException(404, "Запись на приём не найдена")
        result = AppointmentResponse.model_validate(obj).model_dump(mode="json")
        self.cache.set(appointment_id, result)
        return result

    def create(self, data):
        obj = self.repo.create(data.model_dump())
        self.cache.publish("appointment.created", obj.id)
        return obj

    def update(self, appointment_id, data):
        obj = self.repo.get(appointment_id)
        if obj is None:
            raise HTTPException(404, "Запись на приём не найдена")
        result = self.repo.update(obj, data)
        self.cache.invalidate(appointment_id)
        self.cache.publish("appointment.updated", appointment_id)
        return result

    def delete(self, appointment_id):
        obj = self.repo.get(appointment_id)
        if obj is None:
            raise HTTPException(404, "Запись на приём не найдена")
        self.repo.delete(obj)
        self.cache.invalidate(appointment_id)
        self.cache.publish("appointment.deleted", appointment_id)
