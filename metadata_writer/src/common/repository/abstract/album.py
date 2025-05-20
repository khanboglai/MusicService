from abc import ABC, abstractmethod
from src.common.models.album import Album
from src.common.schemas.album import AlbumCreate


class AlbumRepositoryABC(ABC):
    """ Репозиторий альбома (абстрактный базовый класс) """

    @abstractmethod
    async def create_album(self, album: Album) -> Album:
        """ Создать новый альбом """
        ...

    @abstractmethod
    async def get_album_by_id(self, id: int) -> Album:
        """ Получить альбом по ID """
        ...
    
    @abstractmethod
    async def get_albums_by_owner_id(self, owner_id: int) -> list[Album]:
        """ Получить все альбомы исполнителя по его ID """
        ...

    @abstractmethod
    async def remove_album(self, album_id: int) -> int:
        """ Удалить альбом по его ID """
        ...

    @abstractmethod
    async def remove_albums_by_owner_id(self, owner_id: int) -> list[int]:
        """ Удалить все альбомы автора по его ID """
        ...
