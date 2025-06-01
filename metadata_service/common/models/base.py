from abc import ABC, abstractmethod


class Entity(ABC):
    oid: int

    @abstractmethod
    def to_json(self) -> dict:
        """ Представление сущности в виде JSON """
        ...
