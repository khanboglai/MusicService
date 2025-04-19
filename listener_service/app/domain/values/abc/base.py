""" Определение базового объекта-значения """
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar


VT = TypeVar('VT', bound=Any)


@dataclass(frozen=True)
class BaseValueObject(ABC, Generic[VT]):
    """ Базовый объект-значение """
    value: VT

    def __post_init__(self):
        self.validate()

    @abstractmethod
    def validate(self):
        ...
