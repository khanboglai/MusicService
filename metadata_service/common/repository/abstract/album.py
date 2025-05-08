from abc import ABC, abstractmethod
from src.common.models.album import Album


class AlbumRepositoryABC(ABC):
    @abstractmethod
    async def create_album(self, album: Album) -> Album:
        ...

    @abstractmethod
    async def get_album_by_id(self, id: int) -> Album:
        ...
    
    @abstractmethod
    async def get_albums_by_owner(self, owner_id: int) -> list[Album]:
        ...
