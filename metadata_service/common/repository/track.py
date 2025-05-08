from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from src.common.core.logging import logger

from src.common.models.track import Track
from src.common.repository.abstract.track import TrackRepositoryABC
from src.common.exceptions import *


class TrackRepository(TrackRepositoryABC):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_track(self, track: Track) -> Track:
        try:
            logger.info(f"Создание трека {track.title}.")
            self.db.add(track)
            await self.db.commit()
            await self.db.refresh(track)
            logger.info(f"Трек {track.title} успешно создан.")
            return track
        except IntegrityError as e:
            await self.db.rollback()
            raise DatabaseException(f"Ошибка при создании альбома: {e}")

    async def get_track_by_id(self, id: int) -> Track:
        result = await self.db.execute(select(Track).where(Track.oid == id))
        track = result.scalars().first()

        if track is None:
            raise NoSuchTrackException()
        return track
