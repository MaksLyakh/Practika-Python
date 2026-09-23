class Computer:
    def __init__(self, name, processor, ram, storage, price):
        self.name = name
        self.processor = processor
        self.ram = ram
        self.storage = storage
        self.price = price

    def __str__(self):
        return (
            f"Название: {self.name}, "
            f"процессор: {self.processor}, "
            f"RAM: {self.ram} ГБ, "
            f"накопитель: {self.storage}, "
            f"цена: {self.price:.2f} руб."
        )

    def to_dict(self):
        return {
            "name": self.name,
            "processor": self.processor,
            "ram": self.ram,
            "storage": self.storage,
            "price": self.price
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["processor"],
            data["ram"],
            data["storage"],
            data["price"]
        )