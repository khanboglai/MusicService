from pydantic import BaseModel
from typing import Optional
from datetime import date

class AlbumCreate(BaseModel):
    """ Схема создания альбома """
    title: str
    cover_path: Optional[str]
    release_date: date
    author_id: str

class TrackCreate(BaseModel):
    """ Схема создания трека """
    album_id: int
    file_path: str
    explicit: bool
