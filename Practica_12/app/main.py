from app.database import make_engine, make_session_factory, init_db
from app.service import PharmacyService, PharmacyError
from app.seed import seed


def number(prompt, minimum=1):
    while True:
        try:
            value = int(input(prompt))
            if value >= minimum:
                return value
        except ValueError:
            pass
        print(f"Введите целое число от {minimum}")


def show_medicines(items):
    if not items:
        print("Ничего не найдено")
    for m in items:
        print(f"ID {m.id} | {m.name} | {m.article} | {m.price} руб. | остаток {m.stock}")


def menu(service, engine):
    while True:
        print("\n=== АПТЕКА - ЛАБОРАТОРНАЯ №12 ===")
        print("1. Список лекарств (пагинация, сортировка)")
        print("2. Поиск и фильтрация лекарств")
        print("3. Добавить покупателя")
        print("4. Добавить лекарство")
        print("5. Изменить лекарство")
        print("6. Удалить лекарство")
        print("7. Оформить покупку")
        print("8. Покупка по ID")
        print("9. Покупки покупателя")
        print("10. Отменить покупку")
        print("11. Статистика (COUNT/SUM/AVG/MIN/MAX)")
        print("12. Список покупателей")
        print("13. Заполнить тестовыми данными")
        print("0. Выход")
        choice = input("Ваш выбор: ").strip()
        try:
            if choice == "0":
                break
            elif choice == "1":
                page = number("Страница: ")
                size = number("Размер страницы: ")
                sort = input("Сортировка (id/price_asc/price_desc/name): ").strip() or "id"
                show_medicines(service.read(lambda r: r.medicines(page, size, sort=sort)))
            elif choice == "2":
                search = input("Название (можно часть): ").strip()
                max_price = input("Цена не выше (Enter - любая): ").strip()
                min_stock = input("Остаток не меньше (Enter - любой): ").strip()
                show_medicines(service.read(lambda r: r.medicines(search=search,
                    max_price=float(max_price) if max_price else None,
                    min_stock=int(min_stock) if min_stock else None)))
            elif choice == "3":
                print("Создан покупатель ID", service.add_customer(input("ФИО: "), input("Телефон: ")))
            elif choice == "4":
                print("Создано лекарство ID", service.add_medicine(input("Название: "),
                    input("Артикул: "), input("Цена: "), number("Остаток: ", 0)))
            elif choice == "5":
                mid = number("ID лекарства: ")
                price = input("Новая цена (Enter - без изменений): ").strip()
                stock = input("Новый остаток (Enter - без изменений): ").strip()
                service.update_medicine(mid, price or None, int(stock) if stock else None)
                print("Лекарство изменено")
            elif choice == "6":
                service.delete_medicine(number("ID лекарства: "))
                print("Лекарство удалено")
            elif choice == "7":
                cid = number("ID покупателя: ")
                count = number("Сколько разных лекарств: ")
                products = [(number("ID лекарства: "), number("Количество: ")) for _ in range(count)]
                pid, total = service.buy(cid, products)
                print(f"Покупка №{pid} оформлена, сумма {total} руб.")
            elif choice == "8":
                purchase = service.read(lambda r: r.get_purchase(number("ID покупки: ")))
                if purchase is None:
                    print("Покупка не найдена")
                else:
                    print(f"Покупка №{purchase.id}, покупатель {purchase.customer_id}, сумма {purchase.total}, статус {purchase.status}")
                    for item in purchase.items:
                        print(f"  Лекарство {item.medicine_id}: {item.quantity} шт. x {item.unit_price} руб.")
            elif choice == "9":
                purchases = service.read(lambda r: r.purchases(number("ID покупателя: ")))
                for purchase in purchases:
                    print(f"№{purchase.id} | {purchase.total} руб. | {purchase.status}")
                if not purchases:
                    print("Покупок нет")
            elif choice == "10":
                service.cancel_purchase(number("ID покупки: "))
                print("Покупка отменена, остатки восстановлены")
            elif choice == "11":
                for key, value in service.read(lambda r: r.statistics()).items():
                    print(f"{key}: {value}")
            elif choice == "12":
                for customer in service.read(lambda r: r.customers()):
                    print(f"ID {customer.id} | {customer.name} | {customer.phone}")
            elif choice == "13":
                print("Данные добавлены" if seed(engine) else "Данные уже существуют")
            else:
                print("Нет такого пункта")
        except (PharmacyError, ValueError) as exc:
            print("Ошибка:", exc)
        except Exception as exc:
            from sqlalchemy.exc import SQLAlchemyError
            if isinstance(exc, SQLAlchemyError):
                print("Ошибка базы данных:", exc.orig if hasattr(exc, "orig") else exc)
            else:
                raise


def main():
    try:
        engine = make_engine()
        init_db(engine)
        print("Подключение к PostgreSQL успешно")
        menu(PharmacyService(make_session_factory(engine)), engine)
    except Exception as exc:
        print("Не удалось подключиться к БД. Проверьте PostgreSQL и .env:", exc)


if __name__ == "__main__":
    main()
