from pydantic import BaseModel

class TrackCreate(BaseModel):
    title: str
    album_id: int
    explicit: bool
