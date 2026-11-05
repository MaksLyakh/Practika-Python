import json
import os


class ScheduleCache:
    def __init__(self):
        self.url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        try:
            import redis
            self.redis = redis.Redis.from_url(self.url, decode_responses=True, socket_connect_timeout=1)
            self.redis.ping()
        except (ImportError, Exception):
            self.redis = None

    def get(self, key):
        if self.redis is None:
            return None
        try:
            value = self.redis.get(key)
            return json.loads(value) if value else None
        except Exception:
            return None

    def set(self, key, value, seconds=60):
        if self.redis is not None:
            try:
                self.redis.set(key, json.dumps(value, ensure_ascii=False), ex=seconds)
            except Exception:
                pass

    def invalidate(self, doctor_id=None):
        if self.redis is not None:
            try:
                keys = self.redis.keys(f'slots:{doctor_id}:*' if doctor_id else 'slots:*')
                if keys:
                    self.redis.delete(*keys)
            except Exception:
                pass
