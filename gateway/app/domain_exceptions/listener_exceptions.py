from app.domain_exceptions.domain_exception import DomainException


class AgeTooSmallException(DomainException):
    """ Исключение слишком маленького возраста """
    def __init__(self, message: str = "Age must be greater than 18!"):
        super().__init__(message, status_code=422)


class AgeTooBigException(DomainException):
    """ Исключение слишком большого возраста """
    def __init__(self, message: str = "Age must be smaller than 120!"):
        super().__init__(message, status_code=422)


class AgeIncorrectFormat(DomainException):
    """ Исключение неправильного формата даты """
    def __init__(self, message: str = "Age must be in format DD.MM.YYYY"):
        super().__init__(message, status_code=422)


class NameTooLongException(DomainException):
    """ Исключение слишком длинного имени """
    def __init__(self, message: str = "Your name is too long!"):
        super().__init__(message, status_code=422)


class EmptyNameException(DomainException):
    """ Исключение пустого имени """
    def __init__(self, message: str = "Your name must be not empty!"):
        super().__init__(message, status_code=422)


class NotRealNameException(DomainException):
    """ Исключение имени содержащего цифры, спецсимволы и т.д. """
    def __init__(self, message: str = "Your name must containts only chars!"):
        super().__init__(message, status_code=422)


class NotExistException(DomainException):
    """ Исключение для отсутсутствия какого-либо объекта в бд """
    def __init__(self, message: str = "This object doesn't exists in database!"):
        super().__init__(message, status_code=404)


class UniqueException(DomainException):
    """ Исключение для повтора какого-либо объекта в бд """
    def __init__(self, message: str = "This object must be unique in database!"):
        super().__init__(message, status_code=423)
