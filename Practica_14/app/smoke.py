import os
import httpx
from app.config import settings

def main():
    base = os.getenv("API_URL", "http://127.0.0.1:8000")
    with httpx.Client(base_url=base, timeout=10) as client:
        health = client.get("/health")
        health.raise_for_status()
        print("API health:", health.json())
        login = client.post("/auth/login", json={"username": settings.admin_username, "password": settings.admin_password})
        login.raise_for_status()
        headers = {"Authorization": "Bearer " + login.json()["access_token"]}
        data = {"patient":"Тестовый пациент", "doctor":"Тестовый врач",
                "specialty":"Терапевт", "date":"2026-12-31", "time":"15:00:00",
                "room": 101, "status":"scheduled"}
        created = client.post("/appointments", json=data, headers=headers)
        created.raise_for_status()
        aid = created.json()["id"]
        try:
            first = client.get(f"/appointments/{aid}", headers=headers)
            second = client.get(f"/appointments/{aid}", headers=headers)
            first.raise_for_status()
            second.raise_for_status()
            patched = client.patch(f"/appointments/{aid}", json={"status":"completed"}, headers=headers)
            patched.raise_for_status()
            updated = client.get(f"/appointments/{aid}", headers=headers)
            updated.raise_for_status()
            assert updated.json()["status"] == "completed"
            stats = client.get("/appointments/statistics", headers=headers)
            stats.raise_for_status()
            async_result = client.get("/async/statistics")
            async_result.raise_for_status()
            print("POST:", created.status_code, "GET:", first.status_code, second.status_code,
                  "PATCH:", patched.status_code)
            print("Statistics:", stats.json())
            print("Async:", async_result.json())
            print("Проверка реального API: PASSED")
        finally:
            deleted = client.delete(f"/appointments/{aid}", headers=headers)
            print("DELETE:", deleted.status_code)

if __name__ == "__main__":
    main()
