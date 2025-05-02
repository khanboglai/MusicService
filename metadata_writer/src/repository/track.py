from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from src.repository.abstract.track import TrackRepositoryABC
from src.models.track import Track
from src.core.logging import logger

class TrackRepository(TrackRepositoryABC):
    async def create_track(self, track: Track) -> Track:
        try:
            logger.info(f"Создание трека {track.title}")
            self.db.add(track)
            await self.db.commit()
            await self.db.refresh(track) # обновляем, чтобы получить id
            logger.info(f"Трек успешно создан: {track.title}")
            return track
        except IntegrityError as e:
            await self.db.rollback()
            raise ValueError(f"Ошибка при создании трека: {e}")
