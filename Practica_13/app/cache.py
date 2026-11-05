import json

class ClinicCache:
    """Redis String (JSON), Hash (counters), Sorted Set (upcoming timestamps)."""
    def __init__(self, redis_client, ttl=180):
        if ttl < 30:
            raise ValueError("TTL должен быть не менее 30 секунд")
        self.redis = redis_client
        self.ttl = ttl

    @staticmethod
    def appointment_key(appointment_id):
        return f"clinic:appointment:{appointment_id}"

    def get_json(self, key):
        value = self.redis.get(key)
        return json.loads(value) if value is not None else None

    def set_json(self, key, value):
        self.redis.setex(key, self.ttl, json.dumps(value, ensure_ascii=False))

    def delete(self, *keys):
        if keys:
            self.redis.delete(*keys)

    def get_appointment(self, appointment_id):
        return self.get_json(self.appointment_key(appointment_id))

    def set_appointment(self, appointment):
        self.set_json(self.appointment_key(appointment["appointment_id"]), appointment)

    def invalidate_appointment(self, appointment_id):
        self.delete(self.appointment_key(appointment_id))

    def get_doctor(self, doctor_id):
        return self.get_json(f"clinic:doctor:{doctor_id}")

    def set_doctor(self, doctor_id, info):
        self.set_json(f"clinic:doctor:{doctor_id}", info)

    def get_schedule(self, doctor_id, day):
        return self.get_json(f"clinic:schedule:{doctor_id}:{day}")

    def set_schedule(self, doctor_id, day, schedule):
        self.set_json(f"clinic:schedule:{doctor_id}:{day}", schedule)

    def get_upcoming(self, day):
        return self.get_json(f"clinic:upcoming:{day}")

    def set_upcoming(self, day, appointments):
        self.set_json(f"clinic:upcoming:{day}", appointments)

    def invalidate_related(self, appointment):
        if appointment:
            doctor_id = appointment["doctor"]["id"]
            day = appointment["date"]
            self.delete(f"clinic:doctor:{doctor_id}", f"clinic:schedule:{doctor_id}:{day}")
            # Удаляем кэши ближайших приёмов для всех дат, не только даты записи.
            for key in self.redis.scan_iter(match="clinic:upcoming:*"):
                self.redis.delete(key)

    def increment_doctor_views(self, doctor_id):
        key = "clinic:doctor:views"
        self.redis.hincrby(key, doctor_id, 1)
        self.redis.expire(key, 3600)
        return int(self.redis.hget(key, doctor_id))

    def get_doctor_views(self, doctor_id):
        value = self.redis.hget("clinic:doctor:views", doctor_id)
        return int(value) if value is not None else 0

    def store_upcoming_ranking(self, appointments):
        key = "clinic:upcoming:ranking"
        self.redis.delete(key)
        for item in appointments:
            day = item["date"].replace("-", "")
            hour = item["time"].replace(":", "")
            self.redis.zadd(key, {item["appointment_id"]: int(day + hour)})
        self.redis.expire(key, self.ttl)

    def earliest_ids(self, limit=5):
        return self.redis.zrange("clinic:upcoming:ranking", 0, limit - 1)
