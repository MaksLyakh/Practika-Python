import json
import logging
from datetime import date, time
# Redis подключается лениво, чтобы изолированные тесты не требовали сервер.
try:
    from redis.exceptions import RedisError
except ImportError:
    RedisError = ConnectionError
from app.config import settings

log = logging.getLogger(__name__)

class AppointmentCache:
    def __init__(self, client=None, ttl=None):
        if client is None:
            from redis import Redis
            client = Redis.from_url(settings.redis_url, decode_responses=True, socket_connect_timeout=1)
        self.client = client
        self.ttl = ttl if ttl is not None else settings.cache_ttl

    def get(self, appointment_id: int):
        try:
            value = self.client.get(f"lab14:appointment:{appointment_id}")
            return json.loads(value) if value is not None else None
        except RedisError as exc:
            log.warning("Redis GET недоступен: %s", exc)
            return None

    def set(self, appointment_id: int, data: dict):
        try:
            self.client.setex(f"lab14:appointment:{appointment_id}", self.ttl,
                              json.dumps(data, ensure_ascii=False, default=str))
        except RedisError as exc:
            log.warning("Redis SET недоступен: %s", exc)

    def invalidate(self, appointment_id: int):
        try:
            self.client.delete(f"lab14:appointment:{appointment_id}")
        except RedisError as exc:
            log.warning("Redis DELETE недоступен: %s", exc)

    def publish(self, event: str, appointment_id: int):
        try:
            self.client.publish("lab14:events", json.dumps({"event": event, "appointment_id": appointment_id}))
        except RedisError as exc:
            log.warning("Redis Pub/Sub недоступен: %s", exc)

_cache = None

def get_cache():
    global _cache
    if _cache is None:
        _cache = AppointmentCache()
    return _cache
