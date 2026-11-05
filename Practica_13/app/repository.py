from copy import deepcopy
from pymongo import ASCENDING, DESCENDING
from pymongo.errors import DuplicateKeyError
from app.models import validate_appointment

class AppointmentRepository:
    def __init__(self, collection):
        self.collection = collection

    def create_indexes(self):
        self.collection.create_index([("appointment_id", ASCENDING)], unique=True, name="unique_appointment_id")
        self.collection.create_index([("doctor.id", ASCENDING), ("date", ASCENDING), ("time", ASCENDING)], name="doctor_schedule")
        self.collection.create_index([("status", ASCENDING), ("date", ASCENDING)], name="status_date")

    def create(self, data):
        validate_appointment(data)
        self.collection.insert_one(deepcopy(data))
        return data["appointment_id"]

    def get(self, appointment_id):
        return self.collection.find_one({"appointment_id": appointment_id}, {"_id": 0})

    def list(self, filters=None, limit=50):
        return list(self.collection.find(filters or {}, {"_id": 0}).sort([("date", ASCENDING), ("time", ASCENDING)]).limit(limit))

    def update(self, appointment_id, changes):
        if not changes or any(k in changes for k in ("_id", "appointment_id")):
            raise ValueError("Изменение идентификатора запрещено")
        old = self.get(appointment_id)
        if old is None:
            return None
        new = {**old, **changes}
        validate_appointment(new)
        self.collection.update_one({"appointment_id": appointment_id}, {"$set": changes})
        return self.get(appointment_id)

    def delete(self, appointment_id):
        return self.collection.delete_one({"appointment_id": appointment_id}).deleted_count > 0

    def doctor_schedule(self, doctor_id, day=None):
        query = {"doctor.id": doctor_id}
        if day:
            query["date"] = day
        return self.list(query, 500)

    def upcoming(self, day, limit=10):
        return list(self.collection.find({"date": {"$gte": day}, "status": "scheduled"}, {"_id": 0})
                    .sort([("date", 1), ("time", 1)]).limit(limit))

    def doctor_info(self, doctor_id):
        item = self.collection.find_one({"doctor.id": doctor_id}, {"_id": 0, "doctor": 1, "specialty": 1})
        return item

    def ten_queries(self):
        c = self.collection
        clean = {"_id": 0}
        return {
            "01_filter_status": list(c.find({"status": "scheduled"}, clean).limit(5)),
            "02_filter_specialty": list(c.find({"specialty": "Терапевт"}, clean).limit(5)),
            "03_filter_date": list(c.find({"date": {"$gte": "2026-12-01"}}, clean).limit(5)),
            "04_sort_date_asc": list(c.find({}, clean).sort("date", 1).limit(5)),
            "05_sort_time_desc": list(c.find({}, clean).sort("time", -1).limit(5)),
            "06_limit_three": list(c.find({}, clean).limit(3)),
            "07_nested_doctor": list(c.find({"doctor.id": "D01"}, clean).limit(5)),
            "08_array_prescription": list(c.find({"prescriptions": "Общий анализ крови"}, clean).limit(5)),
            "09_aggregation_by_status": list(c.aggregate([{"$group": {"_id": "$status", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}])),
            "10_aggregation_by_specialty": list(c.aggregate([{"$group": {"_id": "$specialty", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}])),
        }
