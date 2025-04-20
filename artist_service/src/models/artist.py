import uuid
from datetime import datetime
from base import Entity
from ..value_objects.artist_description import Description


class Artist(Entity):
    __id: uuid.UUID
    __name: str
    __registered_at: datetime.date
    __cover_path: str
    __description: Description


    def __init__(self, name: str, registered_at: datetime.date) -> None:
        super().__init__()
        self.__id = uuid.uuid4()
        self.__name = name
        self.__registered_at = registered_at


    @property # определили свойство
    def id(self) -> uuid.UUID:
        return self.__id
