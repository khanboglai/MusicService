from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from src.common.core.logging import logger
from src.common.models.album import Album
from src.common.repository.abstract.album import AlbumRepositoryABC
from src.common.exceptions import *


class AlbumRepository(AlbumRepositoryABC):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_album(self, album: Album) -> Album:
        try:
            logger.info(f"Создание альбома {album.title}.")
            self.db.add(album)
            await self.db.commit()
            await self.db.refresh(album)
            logger.info(f"Альбом {album.title} успешно создан.")
            return album
        except IntegrityError as e:
            await self.db.rollback()
            raise DatabaseException(f"Ошибка при создании альбома: {e}")

    async def get_album_by_id(self, id: int) -> Album:
        result = await self.db.execute(select(Album).where(Album.oid == id))
        album = result.scalars().first()

        if album is None:
            raise NoSuchAlbumException()
        return album
    
    async def get_albums_by_owner(self, owner_id: int) -> list[Album]:
        ...
