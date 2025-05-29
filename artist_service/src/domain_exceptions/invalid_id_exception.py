""" Исключение при запросе неправильного id """

from src.domain_exceptions.domain_exception import DomainException


class InvalidIdException(DomainException):
    def __init__(self, message: str = "Этот id не найден"):
        super().__init__(message, status_code=404)
