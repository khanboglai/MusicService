""" Определение абстрактного события """
from abc import ABC


class BaseEvent(ABC):
    """ Абстрактное событие """
    event_id: int
