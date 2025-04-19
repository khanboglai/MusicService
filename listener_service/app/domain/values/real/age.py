""" Определение объекта-значения возраста """
from dataclasses import dataclass
from datetime import date

from domain.exceptions.real.age import AgeTooSmallException, AgeTooBigException
from domain.values.abc.base import BaseValueObject


@dataclass
class Age(BaseValueObject):
    """ Объект-значение возраста """
    value: date

    def validate(self):
        today = date.today()
        age = today.year - self.value.year - ((today.month, today.day) < (self.value.month, self.value.day))
        if age < 18:
            raise AgeTooSmallException()
        if age > 120:
            raise AgeTooBigException()
    