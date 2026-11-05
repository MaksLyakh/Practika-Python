from app.models import validate_appointment

class ClinicService:
    def __init__(self, repository, cache):
        self.repo = repository
        self.cache = cache

    def get_appointment(self, appointment_id, with_source=False):
        cached = self.cache.get_appointment(appointment_id)
        if cached is not None:
            return (cached, "Redis HIT") if with_source else cached
        item = self.repo.get(appointment_id)
        if item is not None:
            self.cache.set_appointment(item)
        return (item, "MongoDB MISS") if with_source else item

    def create_appointment(self, item):
        validate_appointment(item)
        appointment_id = self.repo.create(item)
        self.cache.invalidate_related(item)
        return appointment_id

    def update_appointment(self, appointment_id, changes):
        before = self.repo.get(appointment_id)
        updated = self.repo.update(appointment_id, changes)
        if updated is not None:
            self.cache.invalidate_appointment(appointment_id)
            self.cache.invalidate_related(before)
            self.cache.invalidate_related(updated)
        return updated

    def delete_appointment(self, appointment_id):
        before = self.repo.get(appointment_id)
        deleted = self.repo.delete(appointment_id)
        if deleted:
            self.cache.invalidate_appointment(appointment_id)
            self.cache.invalidate_related(before)
        return deleted

    def doctor_schedule(self, doctor_id, day):
        cached = self.cache.get_schedule(doctor_id, day)
        if cached is not None:
            return cached, "Redis HIT"
        result = self.repo.doctor_schedule(doctor_id, day)
        self.cache.set_schedule(doctor_id, day, result)
        return result, "MongoDB MISS"

    def doctor_info(self, doctor_id):
        self.cache.increment_doctor_views(doctor_id)
        cached = self.cache.get_doctor(doctor_id)
        if cached is not None:
            return cached, "Redis HIT"
        info = self.repo.doctor_info(doctor_id)
        if info is not None:
            self.cache.set_doctor(doctor_id, info)
        return info, "MongoDB MISS"

    def upcoming(self, day):
        cached = self.cache.get_upcoming(day)
        if cached is not None:
            return cached, "Redis HIT"
        result = self.repo.upcoming(day)
        self.cache.set_upcoming(day, result)
        self.cache.store_upcoming_ranking(result)
        return result, "MongoDB MISS"
