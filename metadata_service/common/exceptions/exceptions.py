class DomainException(Exception):
    """ Доменное исключение (базовый класс) """
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return self.message

class DatabaseException(DomainException):
    """ Ошибка базы данных """
    def __init__(self, message: str = "Ошибка в работе базы данных"):
        super().__init__(message, status_code=500)

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

class AlbumTrackDublicateException(DomainException):
    """ В альбоме уже есть трек с таким названием """
    def __init__(self, message: str = "В альбоме уже есть трек с таким именем"):
        super().__init__(message, status_code=409)
