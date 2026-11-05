import json
from datetime import date
from pymongo.errors import PyMongoError
from redis.exceptions import RedisError
from app.db import connect
from app.models import make_appointment
from app.seed import seed

def show(value):
    print(json.dumps(value, ensure_ascii=False, indent=2, default=str))

def main():
    try:
        mongo, redis_client, service = connect()
    except (PyMongoError, RedisError, OSError) as exc:
        print(f"Ошибка подключения к MongoDB или Redis: {exc}")
        print("Запустите docker compose up -d и проверьте docker compose ps")
        return
    menu = """
1 - Заполнить базу (24 записи)
2 - Показать все приёмы
3 - Найти приём по ID (Cache-Aside)
4 - Создать приём
5 - Изменить статус приёма
6 - Удалить приём
7 - Расписание врача
8 - Информация о враче
9 - Ближайшие приёмы
10 - Выполнить 10 MongoDB-запросов
11 - Показать индексы
12 - Демонстрация Cache-Aside и инвалидирования
0 - Выход
"""
    try:
        while True:
            print(menu)
            choice = input("Выбор: ").strip()
            try:
                if choice == "0":
                    break
                elif choice == "1":
                    print("Добавлено:", seed(service.repo, service))
                elif choice == "2":
                    show(service.repo.list())
                elif choice == "3":
                    item, source = service.get_appointment(input("ID (например A001): ").strip(), True)
                    print("Источник:", source)
                    show(item)
                elif choice == "4":
                    item = make_appointment(
                        input("ID пациента: "), input("ФИО пациента: "),
                        input("ID врача: "), input("ФИО врача: "),
                        input("Специальность: "), input("Дата YYYY-MM-DD: "),
                        input("Время HH:MM: "),
                        input("Диагноз: "), [x.strip() for x in input("Назначения через запятую: ").split(",") if x.strip()],
                    )
                    print("Создан ID:", service.create_appointment(item))
                elif choice == "5":
                    aid = input("ID: ").strip()
                    show(service.update_appointment(aid, {"status": input("Статус scheduled/completed/cancelled: ").strip()}))
                elif choice == "6":
                    print("Удалено:", service.delete_appointment(input("ID: ").strip()))
                elif choice == "7":
                    data, source = service.doctor_schedule(input("ID врача (D01): ").strip(), input("Дата YYYY-MM-DD: ").strip())
                    print(source); show(data)
                elif choice == "8":
                    data, source = service.doctor_info(input("ID врача (D01): ").strip())
                    print(source); show(data)
                elif choice == "9":
                    data, source = service.upcoming(input("Начальная дата YYYY-MM-DD: ").strip() or date.today().isoformat())
                    print(source); show(data)
                elif choice == "10":
                    for name, result in service.repo.ten_queries().items():
                        print(f"\n{name} ({len(result)} результатов)")
                        show(result[:3])
                elif choice == "11":
                    show(list(service.repo.collection.list_indexes()))
                elif choice == "12":
                    aid = input("ID существующего приёма (A001): ").strip()
                    first, source = service.get_appointment(aid, True)
                    print("Первый запрос:", source)
                    if first is None:
                        print("Запись не найдена")
                        continue
                    _, source = service.get_appointment(aid, True)
                    print("Повторный запрос:", source)
                    original = first["status"]
                    new_status = "completed" if original != "completed" else "scheduled"
                    service.update_appointment(aid, {"status": new_status})
                    _, source = service.get_appointment(aid, True)
                    print("После изменения:", source)
                    service.update_appointment(aid, {"status": original})
                    print("Исходный статус восстановлен")
                else:
                    print("Неизвестный пункт")
            except (ValueError, PyMongoError, RedisError) as exc:
                print("Ошибка:", exc)
    except (EOFError, KeyboardInterrupt):
        print("\nЗавершение работы")
    finally:
        mongo.close()
        redis_client.close()

if __name__ == "__main__":
    main()
