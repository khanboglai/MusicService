from abc import ABC, abstractmethod
from src.models.track import Track

class TrackRepositoryABC(ABC):
    @abstractmethod
    async def create_track(self, track: Track) -> Track:
        ...
