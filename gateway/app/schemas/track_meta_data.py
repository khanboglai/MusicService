from pydantic import BaseModel
from datetime import date


class AlbumCreate(BaseModel):
    title: str
    owner_id: int
    release_date: date

class TrackCreate(BaseModel):
    title: str
    album_id: int
    explicit: bool
    genre_names: list[str]
    