""" Определение базового исключения """



class AplicationException(Exception):
    """ Базовое исключение приложения """
    @property
    def message(self):
        return 'Application error occured!'
    