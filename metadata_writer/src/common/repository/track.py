from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from src.common.core.logging import logger
from src.common.models.track import Track
from src.common.models.album import Album
from src.common.schemas.track import TrackCreate
from src.common.repository.abstract.track import TrackRepositoryABC
from src.common.exceptions import *
from src.common.database.models import Genre

class TrackRepository(TrackRepositoryABC):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_track(self, track: TrackCreate) -> Track:
        try:
            logger.info(f"Создание трека {track.title}.")
            genres = []
            if track.genre_names:
                for name in track.genre_names:
                    result = await self.db.execute(select(Genre).where(Genre._name == name))
                    genre = result.scalars().first()
                    print(genre)
                    if genre is None:
                        genre = Genre(name=name)
                        self.db.add(genre)
                    genres.append(genre)

            result = await self.db.execute(select(Album).where(Album.oid == track.album_id))
            album = result.scalars().first()
            if album is None:
                raise NoSuchAlbumException()

            t = Track(title=track.title, album_id=track.album_id, explicit=track.explicit)
            t.genres = genres

            self.db.add(t)
            await self.db.commit()
            await self.db.refresh(t)
            logger.info(f"Трек {t.title} успешно создан.")
            return t
        except IntegrityError as e:
            await self.db.rollback()
            raise DatabaseException(f"Ошибка при создании трека: {e}")

    async def get_track_by_id(self, id: int) -> Track:
        result = await self.db.execute(select(Track).where(Track.oid == id))
        track = result.scalars().first()

        if track is None:
            raise NoSuchTrackException()
        return track
