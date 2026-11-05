import requests


BASE_URL = "http://127.0.0.1:5000"

HEADERS = {
    "X-API-Key": "secret-key",
    "X-Client-Version": "1.0"
}


def send_request(method: str, path: str, **kwargs):
    """Отправка HTTP-запроса к серверу."""
    try:
        response = requests.request(
            method,
            BASE_URL + path,
            headers=HEADERS,
            timeout=10,
            **kwargs
        )

        print(f"\nHTTP-статус: {response.status_code}")

        if response.status_code == 304:
            print("Данные не изменились")
            return response

        try:
            print("Ответ сервера:")
            print(response.json())
        except ValueError:
            print(response.text)

        return response

    except requests.exceptions.ConnectionError:
        print("\nОшибка: не удалось подключиться к серверу.")
        print("Убедитесь, что Flask-приложение запущено.")

    except requests.exceptions.Timeout:
        print("\nОшибка: сервер не ответил вовремя.")

    except requests.exceptions.RequestException as error:
        print(f"\nОшибка HTTP-запроса: {error}")

    return None


def get_appointments():
    """Получение всех записей."""
    send_request("GET", "/appointments")


def get_appointment():
    """Получение записи по ID."""
    appointment_id = input("Введите ID записи: ").strip()

    send_request("GET", f"/appointments/{appointment_id}")


def create_appointment():
    """Создание новой записи."""
    print("\nВведите данные записи:")

    patient = input("Пациент: ").strip()
    doctor = input("Врач: ").strip()
    specialty = input("Специальность: ").strip()
    date = input("Дата (YYYY-MM-DD): ").strip()
    time = input("Время (HH:MM): ").strip()

    try:
        room = int(input("Кабинет: "))
    except ValueError:
        print("Ошибка: номер кабинета должен быть целым числом.")
        return

    data = {
        "patient": patient,
        "doctor": doctor,
        "specialty": specialty,
        "date": date,
        "time": time,
        "room": room
    }

    send_request("POST", "/appointments", json=data)


def update_appointment():
    """Полное обновление записи."""
    appointment_id = input("Введите ID записи: ").strip()

    print("\nВведите новые данные:")

    patient = input("Пациент: ").strip()
    doctor = input("Врач: ").strip()
    specialty = input("Специальность: ").strip()
    date = input("Дата (YYYY-MM-DD): ").strip()
    time = input("Время (HH:MM): ").strip()

    try:
        room = int(input("Кабинет: "))
    except ValueError:
        print("Ошибка: номер кабинета должен быть целым числом.")
        return

    status = input(
        "Статус (запланирован/подтверждён/завершён/отменён): "
    ).strip()

    data = {
        "patient": patient,
        "doctor": doctor,
        "specialty": specialty,
        "date": date,
        "time": time,
        "room": room,
        "status": status
    }

    send_request(
        "PUT",
        f"/appointments/{appointment_id}",
        json=data
    )


def patch_appointment():
    """Изменение одного поля записи."""
    appointment_id = input("Введите ID записи: ").strip()

    fields = {
        "1": "patient",
        "2": "doctor",
        "3": "specialty",
        "4": "date",
        "5": "time",
        "6": "room",
        "7": "status"
    }

    print("\nВыберите поле:")
    for number, field in fields.items():
        print(f"{number}. {field}")

    choice = input("Ваш выбор: ").strip()

    if choice not in fields:
        print("Неверный номер поля.")
        return

    field = fields[choice]
    value = input("Новое значение: ").strip()

    if field == "room":
        try:
            value = int(value)
        except ValueError:
            print("Номер кабинета должен быть целым числом.")
            return

    send_request(
        "PATCH",
        f"/appointments/{appointment_id}",
        json={field: value}
    )


def delete_appointment():
    """Удаление записи."""
    appointment_id = input("Введите ID записи: ").strip()

    confirmation = input(
        "Вы уверены, что хотите удалить запись? (да/нет): "
    ).strip().lower()

    if confirmation == "да":
        send_request(
            "DELETE",
            f"/appointments/{appointment_id}"
        )
    else:
        print("Удаление отменено.")


def search_appointments():
    """Поиск записей по пациенту."""
    patient = input("Введите имя пациента: ").strip()

    try:
        response = requests.get(
            BASE_URL + "/appointments/search",
            headers=HEADERS,
            params={"patient": patient},
            timeout=10
        )

        print(f"\nHTTP-статус: {response.status_code}")
        print(response.json())

    except requests.exceptions.RequestException as error:
        print(f"Ошибка запроса: {error}")
    except ValueError:
        print("Сервер вернул некорректный JSON.")


def get_statistics():
    """Получение статистики записей."""
    send_request("GET", "/appointments/stats")


def get_available():
    """Получение запланированных приёмов."""
    send_request("GET", "/appointments/available")


def get_filtered_appointments():
    """Получение записей с фильтрацией и пагинацией."""
    print("\nПараметры поиска (Enter — значение по умолчанию):")

    status = input("Статус: ").strip()
    doctor = input("Врач: ").strip()
    page = input("Страница (по умолчанию 1): ").strip()
    limit = input("Количество записей (по умолчанию 10): ").strip()
    sort_by = input("Сортировать по (id/date/time/doctor): ").strip()

    params = {}

    if status:
        params["status"] = status
    if doctor:
        params["doctor"] = doctor
    if page:
        params["page"] = page
    if limit:
        params["limit"] = limit
    if sort_by:
        params["sort_by"] = sort_by

    try:
        response = requests.get(
            BASE_URL + "/appointments",
            headers=HEADERS,
            params=params,
            timeout=10
        )

        print(f"\nHTTP-статус: {response.status_code}")
        print(response.json())

    except requests.exceptions.RequestException as error:
        print(f"Ошибка запроса: {error}")
    except ValueError:
        print("Сервер вернул некорректный JSON.")


def show_menu():
    """Вывод главного меню."""
    print("\n" + "=" * 45)
    print("       МЕДИЦИНСКАЯ КЛИНИКА")
    print("=" * 45)
    print("1. Показать все записи")
    print("2. Найти запись по ID")
    print("3. Создать запись")
    print("4. Полностью изменить запись")
    print("5. Изменить отдельное поле")
    print("6. Удалить запись")
    print("7. Поиск по пациенту")
    print("8. Статистика записей")
    print("9. Запланированные приёмы")
    print("10. Фильтрация и пагинация")
    print("0. Выход")
    print("=" * 45)


def main():
    actions = {
        "1": get_appointments,
        "2": get_appointment,
        "3": create_appointment,
        "4": update_appointment,
        "5": patch_appointment,
        "6": delete_appointment,
        "7": search_appointments,
        "8": get_statistics,
        "9": get_available,
        "10": get_filtered_appointments
    }

    while True:
        show_menu()

        choice = input("Выберите действие: ").strip()

        if choice == "0":
            print("Работа клиента завершена.")
            break

        action = actions.get(choice)

        if action is None:
            print("Неверный пункт меню.")
        else:
            action()


if __name__ == "__main__":
    main()
