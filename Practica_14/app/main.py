import logging
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import settings
from app.database import init_db
from app.models.appointment import Appointment
from app.routers.appointments import router as appointment_router
from app.routers.auth import router as auth_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Медицинская клиника - REST API", version="1.0.0",
              description="Лабораторная №14, вариант 15. FastAPI + PostgreSQL + Redis + JWT.",
              lifespan=lifespan)
app.include_router(auth_router)
app.include_router(appointment_router)

@app.get("/health", tags=["Служебные"], summary="Проверка работы API")
async def health():
    return {"status": "ok"}

@app.get("/async/statistics", tags=["Асинхронность"], summary="Асинхронный SQLAlchemy и PostgreSQL")
async def async_statistics():
    engine = create_async_engine(settings.async_database_url)
    try:
        async with async_sessionmaker(engine)() as session:
            total = await session.scalar(select(func.count(Appointment.id)))
            return {"total": total or 0, "driver": "asyncpg", "mode": "async"}
    finally:
        await engine.dispose()

@app.get("/external-data", tags=["Дополнительно"], summary="Запрос к внешнему HTTP API")
async def external_data():
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get("https://api.github.com/zen", headers={"Accept": "text/plain"})
            response.raise_for_status()
            return {"source": "GitHub Zen API", "message": response.text}
    except httpx.HTTPError:
        raise HTTPException(503, "Внешний API временно недоступен")
