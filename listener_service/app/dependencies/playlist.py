from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.connect import get_session
from database.repository.abc.playlist import BasePlaylistRepo
from database.repository.real.playlist import PlaylistRepository


def get_playlist_repository(db: AsyncSession = Depends(get_session)) -> BasePlaylistRepo:
    return PlaylistRepository(db)

class PlaylistRepositoryFactory:
    @staticmethod
    async def create(db: AsyncSession = Depends(get_session), use_cahce: bool = False, redis_client = None) -> BasePlaylistRepo:
        if use_cahce and redis_client:
            return ...
        return PlaylistRepository(db)
