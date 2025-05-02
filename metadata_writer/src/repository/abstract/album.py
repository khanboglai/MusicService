from abc import ABC, abstractmethod
from src.models.album import Album

class AlbumRepositoryABC(ABC):
    @abstractmethod
    async def create_album(self, album: Album) -> Album:
        ...
