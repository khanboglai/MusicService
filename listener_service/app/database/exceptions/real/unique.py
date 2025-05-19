from database.exceptions.abc.base import DatabaseException

class UniqueException(DatabaseException):
    @property
    def message(self):
        return 'This object must be unique in database'
    