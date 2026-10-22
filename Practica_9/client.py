import socket

from protocol import send_message, receive_message
from exceptions import ProtocolError


HOST = "127.0.0.1"
PORT = 5000
TIMEOUT = 60


def show_menu():
    print("\n===== СИСТЕМА СТРАХОВАНИЯ =====")
    print("1. Создать страховой полис")
    print("2. Найти полис по ID")
    print("3. Показать все полисы")
    print("4. Изменить статус полиса")
    print("5. Удалить полис")
    print("6. Найти полисы по имени клиента")
    print("7. Рассчитать стоимость полиса")
    print("0. Выход")


def create_request(choice):
    data = {}

    if choice == "1":
        command = "create_policy"
        data = {
            "policy_id": int(input("ID полиса: ")),
            "client_name": input("Имя клиента: "),
            "insurance_type": input("Тип страхования: "),
            "amount": float(input("Страховая сумма: ")),
            "duration_months": int(input("Срок в месяцах: "))
        }

    elif choice == "2":
        command = "get_policy"
        data = {
            "policy_id": int(input("ID полиса: "))
        }

    elif choice == "3":
        command = "get_all_policies"

    elif choice == "4":
        command = "update_status"

        print("\nДоступные статусы:")
        print("1. Активен")
        print("2. Истёк")
        print("3. Отменён")

        statuses = {
            "1": "Активен",
            "2": "Истёк",
            "3": "Отменён"
        }

        data = {
            "policy_id": int(input("ID полиса: ")),
            "status": statuses.get(
                input("Выберите статус: "), ""
            )
        }

    elif choice == "5":
        command = "delete_policy"
        data = {
            "policy_id": int(input("ID полиса: "))
        }

    elif choice == "6":
        command = "find_by_client"
        data = {
            "client_name": input("Имя клиента: ")
        }

    elif choice == "7":
        command = "calculate_cost"
        data = {
            "policy_id": int(input("ID полиса: "))
        }

    else:
        return None

    return {
        "command": command,
        "data": data
    }


def print_policy(policy):
    print("-" * 35)
    print(f"ID: {policy['id']}")
    print(f"Клиент: {policy['client_name']}")
    print(f"Тип страхования: {policy['insurance_type']}")
    print(f"Страховая сумма: {policy['amount']}")
    print(f"Срок: {policy['duration_months']} мес.")
    print(f"Статус: {policy['status']}")


def show_response(response):
    if response.get("status") == "error":
        print("\nОшибка:", response.get("error", "Неизвестная ошибка"))
        return

    data = response.get("data")

    print("\n===== ОТВЕТ СЕРВЕРА =====")

    if isinstance(data, list):
        if not data:
            print("Полисы не найдены")
        else:
            for policy in data:
                print_policy(policy)

    elif isinstance(data, dict):
        if "id" in data:
            print_policy(data)

        elif "cost" in data:
            print("Расчёт стоимости страхования:")
            print(f"ID полиса: {data['policy_id']}")
            print(f"Страховая сумма: {data['insurance_amount']}")
            print(f"Срок: {data['duration_months']} мес.")
            print(f"Годовой тариф: {data['annual_rate'] * 100}%")
            print(f"Стоимость: {data['cost']:.2f} руб.")

        else:
            print(data.get("message", data))

    else:
        print(data)


def start_client():
    try:
        with socket.create_connection(
            (HOST, PORT),
            timeout=5
        ) as client_socket:

            client_socket.settimeout(TIMEOUT)
            print("Успешное подключение к серверу!")

            while True:
                show_menu()
                choice = input("\nВыберите действие: ")

                if choice == "0":
                    print("Завершение работы клиента")
                    break

                try:
                    request = create_request(choice)

                    if request is None:
                        print("Неизвестная команда")
                        continue

                    send_message(client_socket, request)
                    response = receive_message(client_socket)
                    show_response(response)

                except ValueError:
                    print("Ошибка: введено некорректное число")

                except socket.timeout:
                    print("Ошибка: сервер не ответил вовремя")
                    break

                except (ProtocolError, OSError) as error:
                    print(f"Ошибка обмена данными: {error}")
                    break

    except OSError as error:
        print(f"Не удалось подключиться к серверу: {error}")

    except (KeyboardInterrupt, EOFError):
        print("\nРабота клиента завершена")


if __name__ == "__main__":
    start_client()
