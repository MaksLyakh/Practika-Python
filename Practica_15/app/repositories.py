from sqlalchemy import select
from .models import Medicine, Category, Purchase
class MedicineRepository:
    def __init__(self, db): self.db=db
    def list(self, search='', category_id=None, min_price=None, max_price=None, sort='name'):
        q=select(Medicine)
        if search: q=q.where(Medicine.name.ilike(f'%{search}%'))
        if category_id: q=q.where(Medicine.category_id==category_id)
        if min_price is not None: q=q.where(Medicine.price>=min_price)
        if max_price is not None: q=q.where(Medicine.price<=max_price)
        q=q.order_by({'name':Medicine.name.asc(),'price_asc':Medicine.price.asc(),'price_desc':Medicine.price.desc(),'stock':Medicine.stock.desc()}.get(sort,Medicine.name.asc()))
        return self.db.scalars(q).all()
    def get(self, ident): return self.db.get(Medicine, ident)
    def create(self, **data):
        item=Medicine(**data);self.db.add(item);self.db.commit();self.db.refresh(item);return item
    def delete(self, item): self.db.delete(item);self.db.commit()
class CategoryRepository:
    def __init__(self,db): self.db=db
    def list(self): return self.db.scalars(select(Category).order_by(Category.name)).all()
class PurchaseRepository:
    def __init__(self,db): self.db=db
    def list(self): return self.db.scalars(select(Purchase).order_by(Purchase.id.desc())).all()
