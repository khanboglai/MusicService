from datetime import date

from src.common.models.base import Entity
from src.common.models.track import Track

class Album(Entity):
    """ Сущность альбом """
    _title: str
    _owner_id: int
    _release_date: date

    def __init__(self, title: str, owner_id: int, release_date: date):
        """ Конструктор объекта альбома """
        self._title = title
        self._owner_id = owner_id
        self._release_date = release_date

    def to_json(self) -> dict:
        return {
            "title": self.title,
            "owner_id": self.owner_id,
            "release_date": str(self.release_date),
        }

    @property
    def title(self) -> str:
        """ Название альбома """
        return self._title
    
    @property
    def owner_id(self) -> int:
        """ ID исполнителя, которому принадлежит альбом """
        return self._owner_id
    
    @property
    def release_date(self) -> date:
        """ Дата релиза альбома """
        return self._release_date
