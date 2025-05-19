from pydantic import BaseModel

class TrackCreate(BaseModel):
    title: str
    album_id: int
    explicit: bool
    genre_names: list[str]
