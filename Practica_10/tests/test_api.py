def test_index(client):
    """Проверка главной страницы API."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["resource"] == "/appointments"


def test_get_empty_appointments(client, headers):
    """Получение пустого списка записей."""
    response = client.get(
        "/appointments",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json["items"] == []
    assert response.json["total"] == 0


def test_create_appointment(client, headers, sample_appointment):
    """Создание записи через POST."""
    response = client.post(
        "/appointments",
        json=sample_appointment,
        headers=headers
    )

    assert response.status_code == 201
    assert response.json["data"]["id"] == 1
    assert response.json["data"]["patient"] == "Иван Петров"
    assert response.headers["Location"] == "/appointments/1"


def test_get_appointment_by_id(client, headers, sample_appointment):
    """Получение записи по ID."""
    client.post(
        "/appointments",
        json=sample_appointment,
        headers=headers
    )

    response = client.get(
        "/appointments/1",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json["data"]["doctor"] == "Алексей Смирнов"


def test_get_nonexistent_appointment(client, headers):
    """Проверка ответа 404."""
    response = client.get(
        "/appointments/999",
        headers=headers
    )

    assert response.status_code == 404
    assert response.json["success"] is False


def test_create_invalid_appointment(client, headers):
    """Проверка ответа 400 при некорректных данных."""
    response = client.post(
        "/appointments",
        json={"patient": "Иван Петров"},
        headers=headers
    )

    assert response.status_code == 400
    assert response.json["success"] is False


def test_create_conflicting_appointment(
    client, headers, sample_appointment
):
    """Проверка ответа 409 при конфликте записей."""
    client.post(
        "/appointments",
        json=sample_appointment,
        headers=headers
    )

    second = sample_appointment.copy()
    second["patient"] = "Мария Иванова"

    response = client.post(
        "/appointments",
        json=second,
        headers=headers
    )

    assert response.status_code == 409
    assert response.json["success"] is False


def test_put_appointment(client, headers, sample_appointment):
    """Полное обновление записи через PUT."""
    client.post(
        "/appointments",
        json=sample_appointment,
        headers=headers
    )

    updated = sample_appointment.copy()
    updated["patient"] = "Мария Иванова"

    response = client.put(
        "/appointments/1",
        json=updated,
        headers=headers
    )

    assert response.status_code == 200
    assert response.json["data"]["patient"] == "Мария Иванова"


def test_patch_appointment(client, headers, sample_appointment):
    """Частичное обновление записи через PATCH."""
    client.post(
        "/appointments",
        json=sample_appointment,
        headers=headers
    )

    response = client.patch(
        "/appointments/1",
        json={"status": "подтверждён"},
        headers=headers
    )

    assert response.status_code == 200
    assert response.json["data"]["status"] == "подтверждён"


def test_delete_appointment(client, headers, sample_appointment):
    """Удаление записи через DELETE."""
    client.post(
        "/appointments",
        json=sample_appointment,
        headers=headers
    )

    response = client.delete(
        "/appointments/1",
        headers=headers
    )

    assert response.status_code == 200

    check = client.get(
        "/appointments/1",
        headers=headers
    )

    assert check.status_code == 404


def test_missing_api_key(client):
    """Проверка запроса без API-ключа."""
    response = client.get(
        "/appointments",
        headers={"X-Client-Version": "1.0"}
    )

    assert response.status_code == 401


def test_invalid_api_key(client):
    """Проверка неправильного API-ключа."""
    response = client.get(
        "/appointments",
        headers={
            "X-Client-Version": "1.0",
            "X-API-Key": "wrong-key"
        }
    )

    assert response.status_code == 401


def test_missing_client_version(client):
    """Проверка отсутствующей версии клиента."""
    response = client.get(
        "/appointments",
        headers={"X-API-Key": "secret-key"}
    )

    assert response.status_code == 400


def test_invalid_client_version(client):
    """Проверка неправильной версии клиента."""
    response = client.get(
        "/appointments",
        headers={
            "X-API-Key": "secret-key",
            "X-Client-Version": "2.0"
        }
    )

    assert response.status_code == 400


def test_filter_by_status(client, headers, sample_appointment):
    """Фильтрация записей по статусу."""
    client.post(
        "/appointments",
        json=sample_appointment,
        headers=headers
    )

    second = sample_appointment.copy()
    second["status"] = "отменён"

    client.post(
        "/appointments",
        json=second,
        headers=headers
    )

    response = client.get(
        "/appointments?status=отменён",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json["total"] == 1
    assert response.json["items"][0]["status"] == "отменён"


def test_pagination(client, headers, sample_appointment):
    """Проверка пагинации API."""
    for index in range(5):
        data = sample_appointment.copy()
        data["time"] = f"{10 + index:02d}:00"

        client.post(
            "/appointments",
            json=data,
            headers=headers
        )

    response = client.get(
        "/appointments?page=2&limit=2",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json["page"] == 2
    assert response.json["limit"] == 2
    assert response.json["total"] == 5
    assert len(response.json["items"]) == 2


def test_invalid_pagination(client, headers):
    """Проверка некорректной страницы."""
    response = client.get(
        "/appointments?page=0",
        headers=headers
    )

    assert response.status_code == 400


def test_search_patient(client, headers, sample_appointment):
    """Поиск записи по имени пациента."""
    client.post(
        "/appointments",
        json=sample_appointment,
        headers=headers
    )

    response = client.get(
        "/appointments/search?patient=Иван",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json["data"]) == 1


def test_get_statistics(client, headers, sample_appointment):
    """Получение статистики записей."""
    client.post(
        "/appointments",
        json=sample_appointment,
        headers=headers
    )

    response = client.get(
        "/appointments/stats",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json["data"]["total"] == 1
    assert response.json["data"]["planned"] == 1


def test_get_available(client, headers, sample_appointment):
    """Получение запланированных приёмов."""
    client.post(
        "/appointments",
        json=sample_appointment,
        headers=headers
    )

    response = client.get(
        "/appointments/available",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json["data"]) == 1


def test_get_doctor_appointments(
    client, headers, sample_appointment
):
    """Получение записей определённого врача."""
    client.post(
        "/appointments",
        json=sample_appointment,
        headers=headers
    )

    response = client.get(
        "/appointments/doctor/Алексей Смирнов",
        headers=headers
    )

    assert response.status_code == 200
    assert len(response.json["data"]) == 1


def test_etag(client, headers, sample_appointment):
    """Проверка ETag и ответа 304."""
    client.post(
        "/appointments",
        json=sample_appointment,
        headers=headers
    )

    response = client.get(
        "/appointments/1",
        headers=headers
    )

    assert response.status_code == 200
    assert "ETag" in response.headers

    etag = response.headers["ETag"]

    conditional_headers = headers.copy()
    conditional_headers["If-None-Match"] = etag

    second_response = client.get(
        "/appointments/1",
        headers=conditional_headers
    )

    assert second_response.status_code == 304
    assert second_response.data == b""


def test_etag_changes_after_update(
    client, headers, sample_appointment
):
    """Проверка изменения ETag после обновления записи."""
    client.post(
        "/appointments",
        json=sample_appointment,
        headers=headers
    )

    first_response = client.get(
        "/appointments/1",
        headers=headers
    )

    old_etag = first_response.headers["ETag"]

    client.patch(
        "/appointments/1",
        json={"status": "подтверждён"},
        headers=headers
    )

    second_response = client.get(
        "/appointments/1",
        headers=headers
    )

    new_etag = second_response.headers["ETag"]

    assert old_etag != new_etag


def test_response_time_header(client, headers):
    """Проверка заголовка времени выполнения запроса."""
    response = client.get(
        "/appointments",
        headers=headers
    )

    assert response.status_code == 200
    assert "X-Response-Time" in response.headers


def test_openapi_documentation(client):
    """Проверка доступности документации OpenAPI."""
    response = client.get("/openapi.yaml")

    assert response.status_code == 200
    assert b"openapi: 3.0.3" in response.data
