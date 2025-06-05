""" Определение исключения для запрещения вставки или удаления какого-либо объекта """
from database.exceptions.abc.base import DatabaseException


class ForbiddenDeletingException(DatabaseException):
    """ Исключение для запрещения удаления какого-либо объекта в бд """
    @property
    def message(self):
        return "You can't delete this object!"
    
class ForbiddenInsertingException(DatabaseException):
    """ Исключение для запрещения вставки какого-либо объекта в бд """
    @property
    def message(self):
        return "You can't insert this object!"
    