from typing import Optional
from datetime import datetime
from src.models.base import Entity
from src.value_objects.artist_description import Description


class Artist(Entity):
    __id: int
    __name: str
    __registered_at: datetime.date
    __cover_path: str
    __description: Description


    def __init__(self, name: str, registered_at: datetime.date, cover_path: Optional[str], description: Description) -> None:
        super().__init__()
        self.__id: int # будет автоматически генерироваться в БД
        self.__name = name
        self.__registered_at = registered_at
        self.__cover_path = cover_path
        self.__description = description


    @property # определили свойство
    def id(self) -> int:
        return self.__id
