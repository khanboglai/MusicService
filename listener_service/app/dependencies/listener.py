from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.connect import get_session
from database.repository.abc.listener import BaseListenerRepo
from database.repository.real.listener import ListenerRepository


def get_listener_repository(db: AsyncSession = Depends(get_session)) -> BaseListenerRepo:
    return ListenerRepository(db)

class ListenerRepositoryFactory:
    @staticmethod
    async def create(db: AsyncSession = Depends(get_session), use_cahce: bool = False, redis_client = None) -> BaseListenerRepo:
        if use_cahce and redis_client:
            return ...
        return ListenerRepository(db)
