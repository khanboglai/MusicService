from abc import ABC, abstractmethod
from src.common.models.track import Track
from src.common.schemas.track import TrackCreate


class TrackRepositoryABC(ABC):
    """ Репозиторий треков (абстрактный базовый класс) """

    @abstractmethod
    async def create_track(self, track: TrackCreate) -> Track:
        """ Создать трек """
        ...

    @abstractmethod
    async def get_track_by_id(self, id: int) -> Track:
        """ Получить трек по его ID """
        ...

    @abstractmethod
    async def get_tracks_by_album_id(self, album_id: int) -> list[Track]:
        """ Получить треки из альбома по его ID """
        ...

    @abstractmethod
    async def remove_track(self, track_id: int) -> int:
        """ Удалить трек по его ID """
        ...

    @abstractmethod
    async def get_track_genre(self, track_id: int):
        ...
