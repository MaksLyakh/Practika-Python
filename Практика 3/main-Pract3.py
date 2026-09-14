# Базовый класс сервера
class Server:
    def __init__(self, name, ip, ram, cpu_load):
        self.name = name
        self.ip = ip
        self.ram = ram
        self.cpu_load = cpu_load

    # Свойство для контролируемого доступа к загрузке CPU
    @property
    def cpu_load(self):
        return self._cpu_load

    @cpu_load.setter
    def cpu_load(self, value):
        if value < 0 or value > 100:
            raise ValueError("Загрузка CPU должна быть от 0 до 100%.")
        self._cpu_load = value

    # Общий метод оценки загрузки
    def evaluate_load(self):
        return "Обычная загрузка"

    # Изменение загрузки CPU
    def change_load(self, new_load):
        self.cpu_load = new_load

    # Информация о сервере
    def get_info(self):
        return (
            f"Имя: {self.name}, IP: {self.ip}, RAM: {self.ram} ГБ, "
            f"CPU: {self.cpu_load:.1f}%"
        )

    def __str__(self):
        return self.get_info()


# Веб-сервер
class WebServer(Server):
    def __init__(self, name, ip, ram, cpu_load, requests):
        super().__init__(name, ip, ram, cpu_load)
        self.requests = requests

    # Переопределённый метод оценки загрузки
    def evaluate_load(self):
        if self.cpu_load >= 80 or self.requests >= 10000:
            return "Высокая загрузка"
        elif self.cpu_load >= 50 or self.requests >= 5000:
            return "Средняя загрузка"
        else:
            return "Низкая загрузка"

    def get_info(self):
        return (
            f"WebServer | {super().get_info()}, "
            f"запросов: {self.requests}"
        )


# Сервер базы данных
class DatabaseServer(Server):
    def __init__(self, name, ip, ram, cpu_load, connections):
        super().__init__(name, ip, ram, cpu_load)
        self.connections = connections

    # Переопределённый метод оценки загрузки
    def evaluate_load(self):
        if self.cpu_load >= 80 or self.connections >= 500:
            return "Высокая загрузка"
        elif self.cpu_load >= 50 or self.connections >= 200:
            return "Средняя загрузка"
        else:
            return "Низкая загрузка"

    def get_info(self):
        return (
            f"DatabaseServer | {super().get_info()}, "
            f"подключений: {self.connections}"
        )


# Класс центра обработки данных
class DataCenter:
    def __init__(self, name):
        self.name = name
        self.servers = []

    # Добавление сервера
    def add_server(self, server):
        self.servers.append(server)

    # Вывод всех серверов
    def show_servers(self):
        if len(self.servers) == 0:
            print("Список серверов пуст.")
            return

        for i in range(len(self.servers)):
            print(f"{i + 1}. {self.servers[i]}")

    # Удаление сервера по имени
    def delete_server(self, name):
        for server in self.servers:
            if server.name.lower() == name.lower():
                self.servers.remove(server)
                return True
        return False

    # Поиск сервера по имени
    def find_server(self, name):
        for server in self.servers:
            if server.name.lower() == name.lower():
                return server
        return None

    # Средняя загрузка CPU
    def average_load(self):
        if len(self.servers) == 0:
            return 0

        total = 0

        for server in self.servers:
            total += server.cpu_load

        return total / len(self.servers)

    # Сортировка серверов по загрузке CPU
    def sort_by_load(self):
        return sorted(
            self.servers,
            key=lambda server: server.cpu_load,
            reverse=True
        )


# Ввод загрузки CPU с проверкой
def input_cpu():
    cpu = float(input("Введите загрузку CPU (%): "))

    while cpu < 0 or cpu > 100:
        print("Загрузка CPU должна быть от 0 до 100%.")
        cpu = float(input("Введите загрузку CPU (%): "))

    return cpu


# Создание нового сервера
def create_server(data_center):
    print("1. WebServer")
    print("2. DatabaseServer")

    server_type = input("Выберите тип сервера: ")

    if server_type != "1" and server_type != "2":
        print("Неверный тип сервера.")
        return

    name = input("Введите имя сервера: ")
    ip = input("Введите IP-адрес: ")

    ram = int(input("Введите объём RAM (ГБ): "))

    while ram <= 0:
        print("RAM должна быть больше 0.")
        ram = int(input("Введите объём RAM (ГБ): "))

    cpu = input_cpu()

    if server_type == "1":
        requests = int(input("Введите количество запросов: "))

        while requests < 0:
            print("Количество запросов не может быть отрицательным.")
            requests = int(input("Введите количество запросов: "))

        server = WebServer(name, ip, ram, cpu, requests)

    else:
        connections = int(input("Введите количество подключений: "))

        while connections < 0:
            print("Количество подключений не может быть отрицательным.")
            connections = int(input("Введите количество подключений: "))

        server = DatabaseServer(
            name,
            ip,
            ram,
            cpu,
            connections
        )

    data_center.add_server(server)

    print("Сервер добавлен.")


# Полиморфная оценка загрузки серверов
def show_load_evaluation(data_center):
    if len(data_center.servers) == 0:
        print("Список серверов пуст.")
        return

    for server in data_center.servers:
        print(
            f"{server.name}: "
            f"{server.evaluate_load()}"
        )


# Изменение загрузки выбранного сервера
def change_server_load(data_center):
    name = input("Введите имя сервера: ")

    server = data_center.find_server(name)

    if server is None:
        print("Сервер не найден.")
        return

    new_load = input_cpu()

    server.change_load(new_load)

    print("Загрузка CPU изменена.")


# Вывод статистики
def show_statistics(data_center):
    if len(data_center.servers) == 0:
        print("Список серверов пуст.")
        return

    print(
        f"Количество серверов: "
        f"{len(data_center.servers)}"
    )

    print(
        f"Средняя загрузка CPU: "
        f"{data_center.average_load():.2f}%"
    )

    most_loaded = max(
        data_center.servers,
        key=lambda server: server.cpu_load
    )

    print(
        f"Самый загруженный сервер: "
        f"{most_loaded.name} "
        f"({most_loaded.cpu_load:.1f}%)"
    )


# Основная функция
def main():
    data_center = DataCenter(
        "Основной серверный парк"
    )

    choice = "-1"

    while choice != "0":
        print("\n===== СЕРВЕРНЫЙ ПАРК =====")
        print("1. Создать сервер")
        print("2. Показать серверы")
        print("3. Оценить загрузку серверов")
        print("4. Изменить загрузку сервера")
        print("5. Удалить сервер")
        print("6. Показать статистику")
        print("7. Сортировать по загрузке CPU")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            create_server(data_center)

        elif choice == "2":
            data_center.show_servers()

        elif choice == "3":
            show_load_evaluation(data_center)

        elif choice == "4":
            change_server_load(data_center)

        elif choice == "5":
            name = input(
                "Введите имя сервера для удаления: "
            )

            if data_center.delete_server(name):
                print("Сервер удалён.")
            else:
                print("Сервер не найден.")

        elif choice == "6":
            show_statistics(data_center)

        elif choice == "7":
            sorted_servers = (
                data_center.sort_by_load()
            )

            if len(sorted_servers) == 0:
                print("Список серверов пуст.")
            else:
                for server in sorted_servers:
                    print(server)

        elif choice == "0":
            print("Программа завершена.")

        else:
            print(
                "Ошибка. Выберите пункт от 0 до 7."
            )


if __name__ == "__main__":
    main()