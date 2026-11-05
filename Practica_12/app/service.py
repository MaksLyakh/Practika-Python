from decimal import Decimal, InvalidOperation
from sqlalchemy.exc import IntegrityError
from app.models import Customer, Medicine, Purchase, PurchaseItem
from app.repository import PharmacyRepository


class PharmacyError(Exception):
    pass


class PharmacyService:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def _run(self, action):
        try:
            with self.session_factory.begin() as session:
                return action(session, PharmacyRepository(session))
        except IntegrityError as exc:
            raise PharmacyError("Нарушение ограничений БД: дубликат или неверная связь") from exc

    def add_customer(self, name, phone):
        if not name.strip() or not phone.strip():
            raise PharmacyError("Имя и телефон обязательны")
        def action(session, repo):
            customer = Customer(name=name.strip(), phone=phone.strip())
            session.add(customer)
            session.flush()
            return customer.id
        return self._run(action)

    def add_medicine(self, name, article, price, stock):
        try:
            price = Decimal(str(price))
            stock = int(stock)
        except (ValueError, InvalidOperation):
            raise PharmacyError("Неверная цена или количество")
        if not name.strip() or not article.strip() or not price.is_finite() or price <= 0 or stock < 0:
            raise PharmacyError("Проверьте название, артикул, цену и остаток")
        def action(session, repo):
            medicine = Medicine(name=name.strip(), article=article.strip(), price=price, stock=stock)
            session.add(medicine)
            session.flush()
            return medicine.id
        return self._run(action)

    def update_medicine(self, medicine_id, price=None, stock=None):
        def action(session, repo):
            medicine = repo.get_medicine(medicine_id)
            if medicine is None:
                raise PharmacyError("Лекарство не найдено")
            if price is not None:
                try:
                    value = Decimal(str(price))
                except InvalidOperation:
                    raise PharmacyError("Неверная цена")
                if not value.is_finite() or value <= 0:
                    raise PharmacyError("Цена должна быть больше нуля")
                medicine.price = value
            if stock is not None:
                if int(stock) < 0:
                    raise PharmacyError("Остаток не может быть отрицательным")
                medicine.stock = int(stock)
            return medicine.id
        return self._run(action)

    def delete_medicine(self, medicine_id):
        def action(session, repo):
            medicine = repo.get_medicine(medicine_id)
            if medicine is None:
                raise PharmacyError("Лекарство не найдено")
            session.delete(medicine)
        return self._run(action)

    def buy(self, customer_id, products):
        # Важно: покупка и списание остатков происходят в одной транзакции.
        if not products:
            raise PharmacyError("В покупке нет лекарств")
        combined = {}
        for medicine_id, quantity in products:
            medicine_id, quantity = int(medicine_id), int(quantity)
            if quantity <= 0:
                raise PharmacyError("Количество должно быть положительным")
            combined[medicine_id] = combined.get(medicine_id, 0) + quantity

        def action(session, repo):
            if repo.get_customer(customer_id) is None:
                raise PharmacyError("Покупатель не найден")
            purchase = Purchase(customer_id=customer_id, total=Decimal("0"), status="paid")
            session.add(purchase)
            session.flush()
            total = Decimal("0")
            for medicine_id in sorted(combined):
                medicine = repo.get_medicine(medicine_id)
                if medicine is None:
                    raise PharmacyError(f"Лекарство {medicine_id} не найдено")
                # Блокировка строк защищает от одновременной продажи одного остатка в PostgreSQL.
                medicine = session.get(Medicine, medicine_id, with_for_update=True, populate_existing=True)
                quantity = combined[medicine_id]
                if medicine.stock < quantity:
                    raise PharmacyError(f"Недостаточно лекарства {medicine.name}: осталось {medicine.stock}")
                medicine.stock -= quantity
                purchase.items.append(PurchaseItem(medicine=medicine, quantity=quantity, unit_price=medicine.price))
                total += medicine.price * quantity
            purchase.total = total
            session.flush()
            return purchase.id, total
        return self._run(action)

    def cancel_purchase(self, purchase_id):
        def action(session, repo):
            purchase = repo.get_purchase(purchase_id)
            if purchase is None:
                raise PharmacyError("Покупка не найдена")
            if purchase.status != "paid":
                raise PharmacyError("Покупка уже отменена")
            for item in purchase.items:
                medicine = repo.get_medicine(item.medicine_id)
                medicine.stock += item.quantity
            purchase.status = "cancelled"
        return self._run(action)

    def read(self, action):
        with self.session_factory() as session:
            return action(PharmacyRepository(session))
