import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv
load_dotenv()
class Base(DeclarativeBase):
    pass
engine = create_engine(os.getenv('DATABASE_URL', 'postgresql+psycopg://lab15:lab15pass@127.0.0.1:5435/pharmacy'), pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
