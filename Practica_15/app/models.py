from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, Numeric, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base
class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    medicines: Mapped[list['Medicine']] = relationship(back_populates='category')
class Medicine(Base):
    __tablename__ = 'medicines'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)
    category: Mapped[Category] = relationship(back_populates='medicines', lazy='selectin')
    purchases: Mapped[list['Purchase']] = relationship(back_populates='medicine', lazy='selectin')
class Purchase(Base):
    __tablename__ = 'purchases'
    id: Mapped[int] = mapped_column(primary_key=True)
    medicine_id: Mapped[int] = mapped_column(ForeignKey('medicines.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    total: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    medicine: Mapped[Medicine] = relationship(back_populates='purchases')
