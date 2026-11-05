from app.models import Customer, Medicine
from app.database import make_engine, make_session_factory, init_db
from sqlalchemy import select


def seed(engine):
    init_db(engine)
    factory = make_session_factory(engine)
    with factory.begin() as session:
        if session.scalar(select(Customer.id).limit(1)) is not None:
            return False
        session.add_all([
            Customer(name="Иван Петров", phone="89990000001"),
            Customer(name="Анна Соколова", phone="89990000002"),
            Customer(name="Павел Смирнов", phone="89990000003"),
        ])
        session.add_all([
            Medicine(name="Парацетамол", article="MED001", price=75, stock=30),
            Medicine(name="Ибупрофен", article="MED002", price=180, stock=20),
            Medicine(name="Активированный уголь", article="MED003", price=55, stock=50),
            Medicine(name="Лоратадин", article="MED004", price=130, stock=15),
            Medicine(name="Физраствор", article="MED005", price=95, stock=25),
            Medicine(name="Бинт стерильный", article="MED006", price=45, stock=40),
        ])
        return True


if __name__ == "__main__":
    print("Демо-данные добавлены" if seed(make_engine()) else "Данные уже есть")
