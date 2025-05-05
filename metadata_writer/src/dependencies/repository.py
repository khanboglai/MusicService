from fastapi.params import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_session

from src.repository.album import AlbumRepository
from src.repository.track import TrackRepository
from src.repository.abstract.album import AlbumRepositoryABC
from src.repository.abstract.track import TrackRepositoryABC


def get_album_repository(db: AsyncSession = Depends(get_session)) -> AlbumRepositoryABC:
    return AlbumRepository(db)

def get_track_repository(db: AsyncSession = Depends(get_session)) -> TrackRepositoryABC:
    return TrackRepository(db)
