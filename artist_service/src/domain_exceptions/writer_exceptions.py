from src.domain_exceptions.domain_exception import DomainException


class NoSuchAlbumException(DomainException):
    """ Альбом отсутствует """
    def __init__(self, message: str = "Запрашиваемый альбом не существует"):
        super().__init__(message, status_code=404)

class NoSuchTrackException(DomainException):
    """ Трек отсутствует """
    def __init__(self, message: str = "Запрашиваемый трек не существует"):
        super().__init__(message, status_code=404)