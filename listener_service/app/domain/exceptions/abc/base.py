""" Определение базового исключения """
from dataclasses import dataclass


@dataclass
class AplicationException(Exception):
    """ Базовое исключение приложения """
    @property
    def message(self):
        return 'Application error occured!'
    