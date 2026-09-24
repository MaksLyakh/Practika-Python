class Computer:
    def __init__(self, name, processor, ram, storage, price):
        if ram <= 0:
            raise ValueError("Объём RAM должен быть больше 0.")

        if storage <= 0:
            raise ValueError("Объём накопителя должен быть больше 0.")

        if price <= 0:
            raise ValueError("Цена должна быть больше 0.")

        self.name = name
        self.processor = processor
        self.ram = ram
        self.storage = storage
        self.price = price

    def get_type(self):
        return "Обычный"

    def __str__(self):
        return (
            f"{self.name} | {self.get_type()} | "
            f"CPU: {self.processor} | "
            f"RAM: {self.ram} ГБ | "
            f"SSD: {self.storage} ГБ | "
            f"Цена: {self.price:.2f} руб."
        )


class GamingComputer(Computer):
    def get_type(self):
        return "Игровой"


class OfficeComputer(Computer):
    def get_type(self):
        return "Офисный"