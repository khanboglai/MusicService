"""Session maker with database"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from config.settings import settings 

""" Session creating with database"""
URL_DATABASE = settings.postgres_dsn

engine = create_async_engine(URL_DATABASE)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True