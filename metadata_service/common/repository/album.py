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
        logger.info(f"Создание альбома {album.title}...")
        try:
            result = await self.db.execute(select(Album).where(Album._title == album.title, Album._owner_id == album.owner_id))
            same_album = result.scalars().first()
            if same_album is not None:
                raise OwnerAlbumDublicateException(f"У пользователя с ID = {same_album.owner_id} уже есть альбом с названием {same_album.title}")
            
            self.db.add(album)
            await self.db.commit()
            await self.db.refresh(album)
            return album
        except IntegrityError as e:
            await self.db.rollback()
            raise DatabaseException(f"Ошибка при создании альбома: {e}")

    async def get_album_by_id(self, id: int) -> Album:
        logger.info(f"Получение альбома с ID {id}...")
        result = await self.db.execute(select(Album).where(Album.oid == id))
        album = result.scalars().first()

        if album is None:
            raise NoSuchAlbumException(f"Альбом с ID {id} не существует")
        return album
    
    async def get_albums_by_owner_id(self, owner_id: int) -> list[Album]:
        logger.info(f"Создание альбомов автора с ID {owner_id}...")
        result = await self.db.execute(select(Album).where(Album._owner_id == owner_id))
        albums = result.scalars().all()

        if albums is None:
            albums = []
        return albums
    
    async def get_all_albums(self) -> list[Album]:
        logger.info(f"Получение всех альбомов на площадке...")
        result = await self.db.execute(select(Album))
        albums = result.scalars().all()

        if albums is None:
            albums = []
        return albums

    async def remove_album(self, album_id: int) -> int:
        logger.info(f"Удаление альбома с ID {album_id}...")
        try:
            album = await self.get_album_by_id(album_id)
            id = album.oid
            await self.db.delete(album)
            await self.db.commit()
            return id
        except IntegrityError as e:
            raise DatabaseException(f"Ошибка удаления альбома: {e}")

    async def remove_albums_by_owner_id(self, owner_id: int) -> list[int]:
        logger.info(f"Удаление альбомов от автора с ID {owner_id}...")
        try:
            albums = await self.get_albums_by_owner_id(owner_id)
            ids = [album.oid for album in albums]

            for album in albums:
                await self.db.delete(album)
            await self.db.commit()
            return ids
        except IntegrityError as e:
            raise DatabaseException(f"Ошибка удаления альбомов: {e}")
