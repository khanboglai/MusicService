""" Определение базового объекта-значения """
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar


VT = TypeVar('VT', bound=Any)


class BaseValueObject(ABC, Generic[VT]):
    """ Базовый объект-значение """
    value: VT

    def __init__(self, value: VT, skip_validation: bool = False):
        self.value = value
        if not skip_validation:
            self.validate()

    @abstractmethod
    def validate(self):
        ...
