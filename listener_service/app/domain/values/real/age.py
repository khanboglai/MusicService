""" Определение объекта-значения возраста """
from datetime import date, datetime

from domain.exceptions.real.age import (
    AgeTooSmallException,
    AgeTooBigException,
    AgeIncorrectFormat
)
from domain.values.abc.base import BaseValueObject


class Age(BaseValueObject):
    """ Объект-значение возраста """
    value: date

    def validate(self):
        try:
            self.value = datetime.strptime(str(self.value), '%d.%m.%Y').date()
        except ValueError:
            raise AgeIncorrectFormat()
        today = date.today()
        age = today.year - self.value.year - ((today.month, today.day) < (self.value.month, self.value.day))
        if age < 18:
            raise AgeTooSmallException()
        if age > 120:
            raise AgeTooBigException()
        
    def __composite_values__(self):
        return (self.value, )
    