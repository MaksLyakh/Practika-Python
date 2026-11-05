from decimal import Decimal, InvalidOperation
from sqlalchemy.exc import IntegrityError
from .repositories import MedicineRepository
from .models import Category, Purchase
class ValidationError(Exception): pass
class ConflictError(Exception): pass
class PharmacyService:
    def __init__(self, db): self.db=db;self.repo=MedicineRepository(db)
    def parse(self,data):
        try:
            name=str(data['name']).strip(); price=Decimal(str(data['price'])); stock=int(data['stock']); category_id=int(data['category_id'])
            if not name or len(name)>160 or price<=0 or stock<0: raise ValueError()
            if self.db.get(Category,category_id) is None: raise ValueError()
            return dict(name=name,price=price,stock=stock,category_id=category_id)
        except (KeyError,ValueError,TypeError,InvalidOperation): raise ValidationError('Проверьте название, цену, остаток и категорию')
    def create(self,data): return self.repo.create(**self.parse(data))
    def update(self,item,data):
        values=self.parse(data)
        for k,v in values.items(): setattr(item,k,v)
        self.db.commit();self.db.refresh(item);return item
    def delete(self,item):
        if item.purchases: raise ConflictError('Нельзя удалить лекарство, по которому есть покупки')
        self.repo.delete(item)
    def purchase(self,item,quantity):
        try: qty=int(quantity)
        except (TypeError,ValueError): raise ValidationError('Некорректное количество')
        if qty<=0: raise ValidationError('Количество должно быть положительным')
        if item.stock<qty: raise ConflictError('Недостаточно товара на складе')
        item.stock-=qty
        order=Purchase(medicine_id=item.id,quantity=qty,total=item.price*qty)
        self.db.add(order);self.db.commit();self.db.refresh(order);return order
