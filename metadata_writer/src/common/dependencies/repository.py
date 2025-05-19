from sqlalchemy.exc import IntegrityError

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.common.database.session import get_session
from src.common.repository.abstract.album import AlbumRepositoryABC
from src.common.repository.abstract.track import TrackRepositoryABC
from src.common.repository.album import AlbumRepository
from src.common.repository.track import TrackRepository


def get_album_repository(db: AsyncSession = Depends(get_session)) -> AlbumRepositoryABC:
    return AlbumRepository(db)

def get_track_repository(db: AsyncSession = Depends(get_session)) -> TrackRepositoryABC:
    return TrackRepository(db)
