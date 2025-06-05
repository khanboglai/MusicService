from app.domain_exceptions.domain_exception import DomainException


class InvalidDescriptionSize(DomainException):
    def __init__(self, message: str = "Текст описания слишком большой"):
        super().__init__(message, status_code=409)
