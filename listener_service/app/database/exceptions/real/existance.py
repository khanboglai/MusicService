""" Определение исключения для отсутсутствия какого-либо объекта в бд """
from database.exceptions.abc.base import DatabaseException


class NotExistException(DatabaseException):
    """ Исключение для отсутсутствия какого-либо объекта в бд """
    @property
    def message(self):
        return "This object doesn't exists in database"