from app.domain_exceptions.domain_exception import DomainException


class StreamingException(DomainException):
    def __init__(self, message: str = "Внутрення проблема стримингого сервиса"):
        super().__init__(message, status_code=500)
