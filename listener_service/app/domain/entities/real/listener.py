""" Определение сущности слушателя """
from dataclasses import dataclass, field
from datetime import datetime

from domain.entities.abc.base import BaseEntity
from domain.values.real.name import Name
from domain.values.real.age import Age


@dataclass
class Listener(BaseEntity):
    """ Сущность слушателя """
    first_name: Name
    last_name: Name
    birth_date: Age
    subscription: bool

    @classmethod
    def add_listener(cls, first_name: Name, last_name: Name, birth_date: Age):
        new_listener = cls(first_name=first_name, last_name=last_name, birth_date=birth_date, subscription=False)
        return new_listener
