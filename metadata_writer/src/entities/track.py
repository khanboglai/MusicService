from src.entities.base import Entity

class Track(Entity):
    __id: int
    __album_id: int
    __title: str
    __explicit: bool

    def __init__(self, album_id: int, title: str, explicit: bool):
        super().__init__()

        self.__id: int
        self.__album_id: int = album_id
        self.__title: str = title
        self.__explicit: bool = explicit

    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def title(self) -> str:
        return self.__title
