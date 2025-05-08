from abc import ABC, abstractmethod
from src.common.models.track import Track


class TrackRepositoryABC(ABC):
    @abstractmethod
    async def create_track(self, track: Track) -> Track:
        ...

    @abstractmethod
    async def get_track_by_id(self, id: int) -> Track:
        ...