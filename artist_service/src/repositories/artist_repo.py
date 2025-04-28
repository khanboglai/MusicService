from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from src.core.logging import logger
from src.models.artist import Artist
from src.repositories.domain_repo import ArtistRepositoryAbc


class ArtistRepository(ArtistRepositoryAbc):
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_artist(self, artist_id: int) -> Artist:
        result = await self.db.execute(select(Artist).where(Artist.oid == artist_id))
        return result.scalars().first()


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
            raise ValueError(f"Ошибка при создании исполнителя: {e}")
