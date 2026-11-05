from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.models import Customer, Medicine, Purchase


class PharmacyRepository:
    def __init__(self, session):
        self.session = session

    def get_customer(self, customer_id):
        return self.session.get(Customer, customer_id)

    def get_medicine(self, medicine_id):
        return self.session.get(Medicine, medicine_id)

    def get_purchase(self, purchase_id):
        return self.session.scalar(select(Purchase).options(selectinload(Purchase.items)).where(Purchase.id == purchase_id))

    def customers(self):
        return self.session.scalars(select(Customer).order_by(Customer.id)).all()

    def medicines(self, page=1, page_size=10, max_price=None, min_stock=None, search=None, sort="id"):
        query = select(Medicine)
        if max_price is not None:
            query = query.where(Medicine.price <= max_price)
        if min_stock is not None:
            query = query.where(Medicine.stock >= min_stock)
        sqlite_cyrillic_search = bool(search) and self.session.bind.dialect.name == "sqlite"
        if search and not sqlite_cyrillic_search:
            query = query.where(Medicine.name.ilike(f"%{search}%"))
        order = {"id": Medicine.id, "price_asc": Medicine.price.asc(),
                 "price_desc": Medicine.price.desc(), "name": Medicine.name.asc()}
        query = query.order_by(order.get(sort, Medicine.id))
        if sqlite_cyrillic_search:
            # SQLite не умеет регистронезависимый LIKE для кириллицы без расширений.
            results = [m for m in self.session.scalars(query).all() if search.casefold() in m.name.casefold()]
            return results[(page - 1) * page_size:page * page_size]
        return self.session.scalars(query.offset((page - 1) * page_size).limit(page_size)).all()

    def purchases(self, customer_id=None):
        query = select(Purchase).order_by(Purchase.id)
        if customer_id is not None:
            query = query.where(Purchase.customer_id == customer_id)
        return self.session.scalars(query).all()

    def statistics(self):
        count, total, avg, min_value, max_value = self.session.execute(
            select(func.count(Purchase.id), func.coalesce(func.sum(Purchase.total), 0),
                   func.avg(Purchase.total), func.min(Purchase.total), func.max(Purchase.total))
            .where(Purchase.status == "paid")
        ).one()
        return {"count": count, "total": total, "average": avg,
                "minimum": min_value, "maximum": max_value}
