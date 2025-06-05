""" Определение исключения для повтора какого-либо объекта в бд """
from database.exceptions.abc.base import DatabaseException

class UniqueException(DatabaseException):
    """ Исключение для повтора какого-либо объекта в бд """
    @property
    def message(self):
        return 'This object must be unique in database'
    