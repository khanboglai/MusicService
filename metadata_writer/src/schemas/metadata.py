from pydantic import BaseModel

class AlbumMetadata(BaseModel):
    """Структура метаданных альбома"""
    artist_id: int
    title: str
    cover_url: str
    release_year: int

class TrackMetadata(BaseModel):
    """Структура метаданных трека"""
    album_id: int
    title: str
    duration: int
    explicit: bool
