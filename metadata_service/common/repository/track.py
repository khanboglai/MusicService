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
        logger.info(f"Создание трека {track.title}...")
        try:
            same_track = await self.db.execute(select(Track).where(Track._title == track.title, Track._album_id == track.album_id))
            if same_track is not None:
                raise AlbumTrackDublicateException(f"В альбоме ID = {track.album_id} уже есть трек с названием {track.title}")
            
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
            return t
        except IntegrityError as e:
            await self.db.rollback()
            raise DatabaseException(f"Ошибка при создании трека: {e}")

    async def get_track_by_id(self, id: int) -> Track:
        logger.info(f"Получение трека с ID {id}...")
        result = await self.db.execute(select(Track).where(Track.oid == id))
        track = result.scalars().first()

        if track is None:
            raise NoSuchTrackException(f"Трек с ID {id} не существует")
        return track

    async def get_tracks_by_album_id(self, album_id: int) -> list[Track]:
        logger.info(f"Получение треков из альбома с ID {album_id}.")
        result = await self.db.execute(select(Track).where(Track._album_id == album_id))
        tracks = result.scalars().all()

        if tracks is None:
            tracks = []
        return tracks

    async def remove_track(self, track_id: int) -> int:
        logger.info(f"Удаление трека с ID{track_id}.")
        try:
            track = await self.get_track_by_id(track_id)
            id = track.oid
            await self.db.delete(track)
            await self.db.commit()
            return id
        except IntegrityError as e:
            raise DatabaseException(f"Ошибка удаления трека: {e}")