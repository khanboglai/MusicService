from abc import ABC, abstractmethod

from src.models.artist import Artist


class ArtistRepositoryAbc(ABC):
    @abstractmethod
    async def get_artist(self, artist_id: int) -> Artist:
        pass

    @abstractmethod
    async def create_artist(self, artist: Artist) -> Artist:
        pass