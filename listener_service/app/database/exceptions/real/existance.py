from database.exceptions.abc.base import DatabaseException


class NotExistException(DatabaseException):
    @property
    def message(self):
        return "This object doesn't exists in database"