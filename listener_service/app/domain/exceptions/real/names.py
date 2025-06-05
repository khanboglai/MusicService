""" Определения исключений связанных с именами """

from domain.exceptions.abc.base import AplicationException


class NameTooLongException(AplicationException):
    """ Исключение слишком длинного имени """
    @property
    def messsage(self):
        return 'Your name is too long!'
    

class EmptyNameException(AplicationException):
    """ Исключение пустого имени """
    @property
    def message(self):
        return 'Your name must be not empty!' 


class NotRealNameException(AplicationException): # неймниг говно, как придумаю что-то получше, переделаю
    """ Исключение имени содержащего цифры, спецсимволы и т.д. """
    @property
    def message(self):
        return 'Your name must containts only chars!'
