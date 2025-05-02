from typing import Optional
from datetime import datetime
from src.models.base import Entity
from src.models.track import Track

class Album(Entity):
    _title: str
    _cover_path: str
    _release_date: datetime.date
    _author_id: int

    def __init__(self,
                 title: str,
                 cover_path: Optional[str],
                 release_date: datetime.date,
                 author_id: int):
        super().__init__()
        self._title = title
        self._cover_path = cover_path
        self._release_date = release_date
        self._author_id = author_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def cover_path(self) -> str:
        return self._cover_path
    
    @property
    def release_date(self) -> datetime.date:
        return self._release_date
    
    @property
    def author_id(self) -> int:
        return self._author_id
