from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.common.database.session import get_session
from src.common.repository.abstract.album import AlbumRepositoryABC
from src.common.repository.album import AlbumRepository


def get_album_repository(db: AsyncSession = Depends(get_session)) -> AlbumRepositoryABC:
    return AlbumRepository(db)

class AlbumRepositoryFactory:
    @staticmethod
    async def create(db: AsyncSession = Depends(get_session), use_cache: bool = False, redis_client=None) -> AlbumRepositoryABC:
        if use_cache and redis_client:
            return ...
        return AlbumRepository(db)
