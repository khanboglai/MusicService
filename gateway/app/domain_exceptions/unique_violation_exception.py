
from app.domain_exceptions.domain_exception import DomainException


class UniqueViolationException(DomainException):
    def __init__(self, message: str = "Check name or email already exists"):
        super().__init__(message, status_code=409)
