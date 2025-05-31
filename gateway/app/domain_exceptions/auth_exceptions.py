from app.domain_exceptions.domain_exception import DomainException

class UserExistanceException(DomainException):
    """ Исключение для отсутствия пользователя в бд """
    def __init__(self, message: str = "Пользователя с таким логином не найдено"):
        super().__init__(message, status_code=404)

class SQLConnectException(DomainException):
    """ Исключение для ошибки подключения к бд """
    def __init__(self, message: str = "Ошибка подключения к серверу"):
        super().__init__(message, status_code=503)

class InvalidLoginPasswordException(DomainException):
    """ Исключение для неправильного логина/пароля """
    def __init__(self, message: str = "Неправильный логин или пароль"):
        super().__init__(message, status_code=401)

class TokenExistanceException(DomainException):
    """ Исключение для отсутсвия access-токена """
    def __init__(self, message: str = "Отсутствует access-токен. Необходима авторизация"):
        super().__init__(message, status_code=401)

class IncorrectTokenDataException(DomainException):
    """ Исключение для некорректных данных в токене """
    def __init__(self, message: str = "Токен содержит некорректные данные."):
        super().__init__(message, status_code=401)

class ExpiredTokenException(DomainException):
    """ Исключение для просроченного токена """
    def __init__(self, message: str = "Срок действия токена истек. Необходима авторизация."):
        super().__init__(message, status_code=401)

class DamagedTokenException(DomainException):
    """ Исключение для поврежденного токена """
    def __init__(self, message: str = "Access-токен повреждён или имеет недопустимую подпись."):
        super().__init__(message, status_code=401)

class UniqueUserException(DomainException):
    """ Исключение для существующего пользователя в бд """
    def __init__(self, message: str = "Пользователь уже существует"):
        super().__init__(message, status_code=409)
