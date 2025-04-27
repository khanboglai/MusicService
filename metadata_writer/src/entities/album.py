from datetime import date
from src.entities.base import Entity

class Album(Entity):
    __id: int
    __title: str
    __release_date: date

    def __init__(self, title: str, release_date: date):
        super().__init__()

        self.__id: int
        self.__title: str = title
        self.__release_date: date = release_date

    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def title(self) -> str:
        return self.__title
    
    @property
    def release_date(self) -> date:
        return self.__release_date
