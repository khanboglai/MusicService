from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.common.database.session import get_session
from src.common.repository.abstract.track import TrackRepositoryABC
from src.common.repository.track import TrackRepository


def get_track_repository(db: AsyncSession = Depends(get_session)) -> TrackRepositoryABC:
    return TrackRepository(db)

class TrackRepositoryFactory:
    @staticmethod
    async def create(db: AsyncSession = Depends(get_session), use_cache: bool = False, redis_client=None) -> TrackRepositoryABC:
        if use_cache and redis_client:
            return ...
        return TrackRepository(db)
