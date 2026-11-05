import os
from pymongo import MongoClient
from redis import Redis
from app.repository import AppointmentRepository
from app.cache import ClinicCache
from app.service import ClinicService

def connect():
    mongo = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017/"), serverSelectionTimeoutMS=3000)
    mongo.admin.command("ping")
    redis_client = Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"), decode_responses=True, socket_connect_timeout=3)
    redis_client.ping()
    repo = AppointmentRepository(mongo["clinic_lab13"]["appointment"])
    repo.create_indexes()
    return mongo, redis_client, ClinicService(repo, ClinicCache(redis_client))
