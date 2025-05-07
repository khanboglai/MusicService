from typing import Optional
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from src.models.base import Entity
from src.value_objects.artist_description import Description


class Artist(Entity):
    _name: str
    _email: str
    _registered_at: datetime.date
    _description: Description
    _user_id: int # получаем id пользователя от сервиса авторизации и регистрации
    # защищенные поля __field мапятся иначе в sqlalchemy, там надо писать название класса еще


    def __init__(self, name: str, email: str, registered_at: datetime.date, description: Description, user_id: int) -> None:
        super().__init__()
        self._name = name
        self._email = email
        self._registered_at = registered_at
        self._description = description
        self._user_id = user_id



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
    def description(self) -> Description:
        return self._description

    # для использования в sql запросах придется использовать hybrid property
    @hybrid_property
    def user_id(self) -> int:
        return self._user_id
