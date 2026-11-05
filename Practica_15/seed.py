from app.database import Base, engine, SessionLocal
from app.models import Category, Medicine
from sqlalchemy import select
Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    if db.scalar(select(Category.id).limit(1)):
        print('Данные уже существуют, повторное заполнение не требуется')
    else:
        cats=[Category(name=n) for n in ('Обезболивающие','Витамины','Простуда','Первая помощь')]
        db.add_all(cats);db.flush()
        entries=[('Парацетамол',89,40,2),('Ибупрофен',149,25,0),('Аспирин',119,18,0),('Витамин C',199,35,1),('Витамин D3',349,22,1),('Комплекс витаминов',499,12,1),('Спрей для горла',279,15,2),('Леденцы для горла',159,32,2),('Солевой спрей',189,20,2),('Бинт стерильный',59,80,3),('Пластырь',79,65,3),('Антисептик',129,45,3)]
        db.add_all([Medicine(name=n,price=p,stock=s,category_id=cats[c].id) for n,p,s,c in entries]);db.commit()
        print('Создано 4 категории и 12 лекарств')
