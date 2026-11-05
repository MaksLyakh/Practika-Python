from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import settings

class Base(DeclarativeBase):
    pass

_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(settings.database_url, pool_pre_ping=True)
    return _engine

def get_db():
    with sessionmaker(bind=get_engine(), expire_on_commit=False)() as db:
        yield db

def init_db():
    from app.models.appointment import Appointment, User, Attachment
    Base.metadata.create_all(bind=get_engine())
