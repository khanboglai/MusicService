from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.connect import get_session
from database.repository.abc.interaction import BaseInteractionRepo
from database.repository.real.interaction import InteractionRepository


def get_interaction_repository(db: AsyncSession = Depends(get_session)) -> BaseInteractionRepo:
    return InteractionRepository(db)

class InteractionRepositoryFactory:
    @staticmethod
    async def create(db: AsyncSession = Depends(get_session), use_cache: bool = False, redis_client = None) -> BaseInteractionRepo:
        if use_cache and redis_client:
            return ...
        return InteractionRepository(db)
    