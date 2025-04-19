""" Определения исключений связанных с возрастом """
from dataclasses import dataclass

from domain.exceptions.abc.base import AplicationException


@dataclass
class AgeTooSmallException(AplicationException):
    """ Исключение слишком маленького возраста """
    @property
    def message(self):
        return 'Age must be greater than 18!'
    

@dataclass
class AgeTooBigException(AplicationException):
    """ Исключение слишком большого возраста """
    @property
    def message(self):
        return 'Age must be smaller than 120!'
