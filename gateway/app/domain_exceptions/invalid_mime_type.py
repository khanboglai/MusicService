""" Исключение для формата файла """

from app.domain_exceptions.domain_exception import DomainException


class InvalidMimeType(DomainException):
    def __init__(self, message: str = "Неверный формат файла"):
        super().__init__(message, status_code=400)
