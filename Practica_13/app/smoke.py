"""Проверка реальных MongoDB и Redis (не mock)."""
from app.db import connect
from app.models import make_appointment

def main():
    mongo, redis_client, service = connect()
    try:
        print("MongoDB ping:", mongo.admin.command("ping"))
        print("Redis ping:", redis_client.ping())
        item = make_appointment(
            "PSMOKE", "Проверка", "DSMOKE", "Тестовый врач", "Терапевт",
            "2026-12-31", "12:00", "Проверка", ["Анализ"], "scheduled", "SMOKE_TEST"
        )
        if service.repo.get("SMOKE_TEST") is not None:
            service.delete_appointment("SMOKE_TEST")
        service.create_appointment(item)
        _, first = service.get_appointment("SMOKE_TEST", True)
        _, second = service.get_appointment("SMOKE_TEST", True)
        service.update_appointment("SMOKE_TEST", {"status": "completed"})
        updated, third = service.get_appointment("SMOKE_TEST", True)
        print("Cache-Aside:", first, "->", second, "->", third)
        print("Обновлённый статус:", updated["status"])
        assert (first, second, third) == ("MongoDB MISS", "Redis HIT", "MongoDB MISS")
        assert updated["status"] == "completed"
        assert service.delete_appointment("SMOKE_TEST")
        print("Проверка реальных баз: PASSED")
    finally:
        mongo.close()
        redis_client.close()

if __name__ == "__main__":
    main()
