""" Определение базового объекта-значения """
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar


VT = TypeVar('VT', bound=Any)


class BaseValueObject(ABC, Generic[VT]):
    """ Базовый объект-значение """
    value: VT

    def __init__(self, value: VT):
        self.value = value
        self.validate()

    @abstractmethod
    def validate(self):
        ...
