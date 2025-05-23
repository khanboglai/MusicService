from src.common.models.base import Entity

class Track(Entity):
    _title: str
    _album_id: int
    _explicit: bool

    def __init__(self, title, album_id, explicit):
        self._title = title
        self._album_id = album_id
        self._explicit = explicit

    def to_json(self) -> dict:
        return {
            "title": self.title,
            "album_id": self.album_id,
            "explicit": self.explicit
        }

    @property
    def title(self) -> str:
        return self._title
    
    @property
    def album_id(self) -> int:
        return self._album_id
    
    @property
    def explicit(self) -> bool:
        return self._explicit
