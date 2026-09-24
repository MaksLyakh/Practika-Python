# Генератор компьютеров определённого типа
def computers_by_type(computers, computer_type):
    for computer in computers:
        if computer.get_type().lower() == computer_type.lower():
            yield computer


# Собственный итератор
class ComputerIterator:
    def __init__(self, computers):
        self.computers = computers
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.computers):
            raise StopIteration

        computer = self.computers[self.index]
        self.index += 1

        return computer