from typing import Optional
from datetime import datetime
from src.models.base import Entity
from src.value_objects.artist_description import Description


class Artist(Entity):
    _name: str
    _email: str
    _registered_at: datetime.date
    _cover_path: str
    _description: Description
    # защищенные поля __field мапятся иначе в sqlalchemy, там надо писать название класса еще


    def __init__(self, name: str, email: str, registered_at: datetime.date, cover_path: Optional[str], description: Description) -> None:
        super().__init__()
        self._name = name
        self._email = email
        self._registered_at = registered_at
        self._cover_path = cover_path
        self._description = description


    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def registered_at(self) -> datetime.date:
        return self._registered_at

    @property
    def cover_path(self) -> str:
        return self._cover_path

    @property
    def description(self) -> Description:
        return self._description
