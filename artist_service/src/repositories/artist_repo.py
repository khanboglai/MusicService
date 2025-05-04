from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from src.core.logging import logger
from src.models.artist import Artist
from src.repositories.domain_repo import ArtistRepositoryABC
from src.domain_exceptions import *


class ArtistRepository(ArtistRepositoryABC):
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_artist_by_id(self, artist_id: int) -> Artist:
        result = await self.db.execute(select(Artist).where(Artist.oid == artist_id))
        artist = result.scalars().first()

        if artist is None:
            raise InvalidIdException(f"Исполнитель с id = {artist_id} не найден")
        return artist


    async def create_artist(self, artist: Artist) -> Artist:
        try:
            logger.info(f"Создание исполнителя {artist.name}")
            self.db.add(artist)
            await self.db.commit()
            await self.db.refresh(artist) # обновляем, чтобы получить id
            logger.info(f"Исполнитель успешно создан: {artist.name}")
            return artist
        except IntegrityError as e:
            await self.db.rollback()
            if "Key (name)" in str(e):
                raise UniqueViolationException(f"Исполнитель {artist.name} уже существует")
            if "Key (email)" in str(e):
                raise UniqueViolationException(f"Исполнитель с почтой {artist.email} уже существует")
            # если какая-то незнакомая ошибка
            raise DatabaseException(f"Ошибка при создании исполнителя: {e}")


    async def delete_artist(self, artist_id: int):

        try:
            artist = await self.get_artist_by_id(artist_id)
            await self.db.delete(artist)
            await self.db.commit()
            return artist.name
        except IntegrityError as e:
            raise DatabaseException(f"Ошибка удаления исполнителя: {e}")

