from app.domain_exceptions.domain_exception import DomainException


class DatabaseException(DomainException):
    def __init__(self, message: str = "Ошибка в работе базы данных"):
        super().__init__(message, status_code=500)
