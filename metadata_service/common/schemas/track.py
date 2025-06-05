from pydantic import BaseModel

class TrackCreate(BaseModel):
    """ Схема создания трека """
    title: str
    album_id: int
    explicit: bool
    genre_names: list[str]
