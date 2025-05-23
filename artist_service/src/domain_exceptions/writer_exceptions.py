from src.domain_exceptions.domain_exception import DomainException


class NoSuchAlbumException(DomainException):
    """ Альбом отсутствует """
    def __init__(self, message: str = "Запрашиваемый альбом не существует"):
        super().__init__(message, status_code=404)

class NoSuchTrackException(DomainException):
    """ Трек отсутствует """
    def __init__(self, message: str = "Запрашиваемый трек не существует"):
        super().__init__(message, status_code=404)

class OwnerAlbumDublicateException(DomainException):
    """ У исполнителя уже есть альбом с таким именем """
    def __init__(self, message: str = "У исполнителя уже существует альбом с таким именем"):
        super().__init__(message, status_code=409)