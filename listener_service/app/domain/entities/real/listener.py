""" Определение сущности слушателя """
from domain.entities.abc.base import BaseEntity
from domain.values.real.name import Name
from domain.values.real.age import Age


class Listener(BaseEntity):
    """ Сущность слушателя """
    user_id: int
    firstname: Name
    lastname: Name
    birthdate: Age
    subscription: bool

    def __init__(self, user_id: int, firstname: Name, lastname: Name, birthdate: Age, subscription: bool):
        self.user_id, self.firstname, self.lastname, self.birthdate, self.subscription = user_id, firstname, lastname, birthdate, subscription 

    @classmethod
    def add_listener(cls, user_id: int, firstname: Name, lastname: Name, birthdate: Age):
        new_listener = cls(user_id=user_id, firstname=firstname, lastname=lastname, birthdate=birthdate, subscription=False)
        return new_listener
