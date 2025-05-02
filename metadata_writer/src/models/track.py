from src.models.base import Entity

class Track(Entity):
    _title: str
    _album_id: int
    _file_path: str 
    _explicit: bool

    def __init__(self, title: str, album_id: int, file_path: str, explicit: bool):
        super().__init__()
        self._title = title
        self._album_id = album_id
        self._file_path = file_path
        self.explicit = explicit

    @property
    def title(self) -> str:
        return self._title
    
    @property
    def album_id(self) -> int:
        return self._album_id

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def explicit(self) -> bool:
        return self._explicit
