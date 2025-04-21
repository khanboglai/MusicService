""" Определение объекта-значения для имени и фамилии (текста) """
import re
from dataclasses import dataclass

from domain.values.abc.base import BaseValueObject
from domain.exceptions.real.names import NameTooLongException, EmptyNameException, NotRealNameException


@dataclass(frozen=True)
class Name(BaseValueObject):
    """ Объект-значение для имени """
    value: str

    def validate(self):
        if not self.value:
            raise EmptyNameException()
        
        if len(self.value) > 20:
            raise NameTooLongException()
        
        if not re.match("^[A-Za-zА-Яа-яЁё]+$", self.value):
            raise NotRealNameException()
