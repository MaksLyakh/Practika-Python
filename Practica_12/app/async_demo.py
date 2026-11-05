"""Дополнительное задание E - AsyncEngine и AsyncSession."""
import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.models import Medicine


async def main():
    load_dotenv()
    url = os.getenv("ASYNC_DATABASE_URL", "postgresql+asyncpg://pharmacy:pharmacy@localhost:5432/pharmacy_db")
    engine = create_async_engine(url)
    try:
        factory = async_sessionmaker(engine)
        async with factory() as session:
            result = await session.scalars(select(Medicine).order_by(Medicine.id).limit(5))
            for medicine in result:
                print(f"{medicine.id}: {medicine.name} - {medicine.price} руб.")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
