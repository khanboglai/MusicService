""" Определение абстрактного события """
from abc import ABC
from uuid import UUID, uuid4


class BaseEvent(ABC):
    """ Абстрактное событие """
    event_id: UUID
