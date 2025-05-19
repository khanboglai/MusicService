from abc import ABC, abstractmethod
from src.common.models.track import Track
from src.common.schemas.track import TrackCreate


class TrackRepositoryABC(ABC):
    @abstractmethod
    async def create_track(self, track: TrackCreate) -> Track:
        ...

    @abstractmethod
    async def get_track_by_id(self, id: int) -> Track:
        ...
