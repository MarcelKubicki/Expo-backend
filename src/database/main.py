from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config


engine = AsyncEngine(create_engine(
    url=Config.DATABASE_URL,
    echo=True
))


async def init_db():
    async with engine.begin() as conn:
        from events.models import Localization, Category, Event, Exhibitor, EventExhibitor
        await conn.run_sync(SQLModel.metadata.create_all)
