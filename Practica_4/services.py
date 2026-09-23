from exceptions import ComputerNotFoundError


class ComputerService:
    def __init__(self, computers):
        self.computers = computers

    def add_computer(self, computer):
        self.computers.append(computer)

    def show_computers(self):
        if len(self.computers) == 0:
            print("Каталог компьютеров пуст.")
            return

        for i in range(len(self.computers)):
            print(f"{i + 1}. {self.computers[i]}")

    def find_computer(self, name):
        for computer in self.computers:
            if computer.name.lower() == name.lower():
                return computer

        raise ComputerNotFoundError(
            f"Компьютер с названием '{name}' не найден."
        )

    def change_computer(self, name, processor, ram, storage, price):
        computer = self.find_computer(name)

        computer.processor = processor
        computer.ram = ram
        computer.storage = storage
        computer.price = price

    def filter_by_ram(self, min_ram):
        result = []

        for computer in self.computers:
            if computer.ram >= min_ram:
                result.append(computer)

        return result

    def sort_by_price(self):
        return sorted(
            self.computers,
            key=lambda computer: computer.price
        )