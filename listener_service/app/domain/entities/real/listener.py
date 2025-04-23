""" Определение сущности слушателя """
from datetime import date

from domain.entities.abc.base import BaseEntity
from domain.values.real.name import Name
from domain.values.real.age import Age


class Listener(BaseEntity):
    """ Сущность слушателя """
    firstname: Name
    lastname: Name
    birthdate: Age
    subscription: bool

    def __init__(self, firstname: Name, lastname: Name, birthdate: Age, subscription: bool):
        self.firstname, self.lastname, self.birthdate, self.subscription = firstname, lastname, birthdate, subscription 

    @classmethod
    def add_listener(cls, firstname: Name, lastname: Name, birthdate: Age):
        new_listener = cls(firstname=firstname, lastname=lastname, birthdate=birthdate, subscription=False)
        return new_listener
