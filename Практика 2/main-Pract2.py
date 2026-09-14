# Добавление нового сервера
def add_server(servers):
    server = {}

    server["name"] = input("Введите имя сервера: ")
    server["ip"] = input("Введите IP-адрес: ")
    server["purpose"] = input("Введите назначение сервера: ")

    ram = int(input("Введите объём RAM (ГБ): "))
    while ram <= 0:
        print("RAM должна быть больше 0.")
        ram = int(input("Введите объём RAM (ГБ): "))

    cpu = float(input("Введите загрузку CPU (%): "))
    while cpu < 0 or cpu > 100:
        print("Загрузка CPU должна быть от 0 до 100.")
        cpu = float(input("Введите загрузку CPU (%): "))

    server["ram"] = ram
    server["cpu"] = cpu

    servers.append(server)

    print("Сервер добавлен.")


# Вывод всех серверов
def show_servers(servers):
    if len(servers) == 0:
        print("Список серверов пуст.")
        return

    for i in range(len(servers)):
        server = servers[i]

        print(
            f"{i + 1}. "
            f"Имя: {server['name']}, "
            f"IP: {server['ip']}, "
            f"Назначение: {server['purpose']}, "
            f"RAM: {server['ram']} ГБ, "
            f"CPU: {server['cpu']:.1f}%"
        )


# Поиск серверов по назначению
def find_by_purpose(servers):
    purpose = input("Введите назначение для поиска: ")

    found = [
        server
        for server in servers
        if server["purpose"].lower() == purpose.lower()
    ]

    if len(found) == 0:
        print("Серверы с таким назначением не найдены.")
    else:
        show_servers(found)


# Фильтрация серверов по загрузке CPU
def filter_by_cpu(servers):
    max_cpu = float(input("Введите максимальную загрузку CPU: "))

    while max_cpu < 0 or max_cpu > 100:
        print("Загрузка CPU должна быть от 0 до 100.")
        max_cpu = float(input("Введите максимальную загрузку CPU: "))

    filtered = [
        server
        for server in servers
        if server["cpu"] <= max_cpu
    ]

    if len(filtered) == 0:
        print("Подходящие серверы не найдены.")
    else:
        show_servers(filtered)


# Сортировка серверов по загрузке CPU
def sort_by_cpu(servers):
    sorted_servers = sorted(
        servers,
        key=lambda server: server["cpu"],
        reverse=True
    )

    show_servers(sorted_servers)


# Вывод статистики
def show_statistics(servers):
    if len(servers) == 0:
        print("Сначала добавьте серверы.")
        return

    total_cpu = 0

    for server in servers:
        total_cpu += server["cpu"]

    average_cpu = total_cpu / len(servers)

    most_loaded = max(
        servers,
        key=lambda server: server["cpu"]
    )

    min_loaded = min(
        servers,
        key=lambda server: server["cpu"]
    )

    print(f"Количество серверов: {len(servers)}")
    print(f"Средняя загрузка CPU: {average_cpu:.2f}%")

    print(
        f"Самый загруженный сервер: "
        f"{most_loaded['name']} "
        f"({most_loaded['cpu']:.1f}%)"
    )

    print(
        f"Наименее загруженный сервер: "
        f"{min_loaded['name']} "
        f"({min_loaded['cpu']:.1f}%)"
    )


# Вывод уникальных назначений серверов
def show_unique_purposes(servers):
    if len(servers) == 0:
        print("Список серверов пуст.")
        return

    purposes = set()

    for server in servers:
        purposes.add(server["purpose"])

    print("Уникальные назначения серверов:")

    for purpose in purposes:
        print(purpose)


# Удаление сервера по имени
def delete_server(servers):
    if len(servers) == 0:
        print("Список серверов пуст.")
        return

    name = input("Введите имя сервера для удаления: ")

    found = False

    for server in servers:
        if server["name"].lower() == name.lower():
            servers.remove(server)
            found = True
            print("Сервер удалён.")
            break

    if found == False:
        print("Сервер с таким именем не найден.")


# Основная функция
def main():
    servers = []

    choice = "-1"

    while choice != "0":
        print("\n===== МЕНЮ =====")
        print("1. Добавить сервер")
        print("2. Показать все серверы")
        print("3. Найти серверы по назначению")
        print("4. Фильтрация по загрузке CPU")
        print("5. Сортировка по загрузке CPU")
        print("6. Показать статистику")
        print("7. Показать уникальные назначения")
        print("8. Удалить сервер")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            add_server(servers)

        elif choice == "2":
            show_servers(servers)

        elif choice == "3":
            find_by_purpose(servers)

        elif choice == "4":
            filter_by_cpu(servers)

        elif choice == "5":
            sort_by_cpu(servers)

        elif choice == "6":
            show_statistics(servers)

        elif choice == "7":
            show_unique_purposes(servers)

        elif choice == "8":
            delete_server(servers)

        elif choice == "0":
            print("Программа завершена.")

        else:
            print("Ошибка. Выберите пункт от 0 до 8.")


if __name__ == "__main__":
    main()