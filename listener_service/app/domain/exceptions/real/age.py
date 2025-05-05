""" Определения исключений связанных с возрастом """
from domain.exceptions.abc.base import AplicationException


class AgeTooSmallException(AplicationException):
    """ Исключение слишком маленького возраста """
    @property
    def message(self):
        return 'Age must be greater than 18!'
    

class AgeTooBigException(AplicationException):
    """ Исключение слишком большого возраста """
    @property
    def message(self):
        return 'Age must be smaller than 120!'


class AgeIncorrectFormat(AplicationException):
    @property
    def message(self):
        return 'Age must be in format DD.MM.YYYY'
