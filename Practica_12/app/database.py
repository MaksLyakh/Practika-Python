import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.models import Base

load_dotenv()
DEFAULT_URL = "postgresql+psycopg://pharmacy:pharmacy@localhost:5432/pharmacy_db"


def make_engine(url=None):
    engine = create_engine(url or os.getenv("DATABASE_URL", DEFAULT_URL), pool_pre_ping=True)
    if engine.dialect.name == "sqlite":
        @event.listens_for(engine, "connect")
        def enable_fk(connection, record):
            connection.execute("PRAGMA foreign_keys=ON")
    return engine


def init_db(engine):
    Base.metadata.create_all(engine)


def make_session_factory(engine):
    return sessionmaker(engine, expire_on_commit=False)
