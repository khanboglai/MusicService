from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from core.config import get_db_url
from contextlib import asynccontextmanager


URL_DATABASE = get_db_url()

engine = create_async_engine(URL_DATABASE)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()

async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

@asynccontextmanager
async def get_db_session():
    async for session in get_session():
        yield session
