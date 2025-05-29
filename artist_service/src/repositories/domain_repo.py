""" Тут прописал абстрактный класс для слоя репозитория исполнителя """

from abc import ABC, abstractmethod
from src.models.artist import Artist


class ArtistRepositoryABC(ABC):
    @abstractmethod
    async def get_artist_by_id(self, artist_id: int) -> Artist:
        pass

    @abstractmethod
    async def create_artist(self, artist: Artist) -> Artist:
        pass

    @abstractmethod
    async def delete_artist(self, artist_id: int) -> Artist:
        pass

    @abstractmethod
    async def get_artist_by_user_id(self, user_id: int) -> Artist:
        pass
