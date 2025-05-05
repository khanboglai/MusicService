from sqlalchemy.exc import IntegrityError

from src.repository.abstract.album import AlbumRepositoryABC
from src.models.album import Album
from src.core.logging import logger


class AlbumRepository(AlbumRepositoryABC):
    async def create_album(self, album: Album) -> Album:
        try:
            logger.info(f"Создание альбома {album.title}")
            self.db.add(album)
            await self.db.commit()
            await self.db.refresh(album)
            logger.info(f"Альбом успешно создан: {album.title}")
            return album
        except IntegrityError as e:
            await self.db.rollback()
            raise ValueError(f"Ошибка при создании альбома: {e}")
