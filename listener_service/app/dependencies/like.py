from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.connect import get_session
from database.repository.abc.like import BaseLikeRepo
from database.repository.real.like import LikeRepository


def get_like_repository(db: AsyncSession = Depends(get_session)) -> BaseLikeRepo:
    return LikeRepository(db)

class LikeRepositoryFactory:
    @staticmethod
    async def create(db: AsyncSession = Depends(get_session), use_cache: bool = False, redis_client = None) -> BaseLikeRepo:
        if use_cache and redis_client:
            return ...
        return LikeRepository(db)
