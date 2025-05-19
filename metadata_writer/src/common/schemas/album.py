from pydantic import BaseModel
from datetime import date

class AlbumCreate(BaseModel):
    title: str
    owner_id: int
    release_date: date

