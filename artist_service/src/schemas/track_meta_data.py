from pydantic import BaseModel


class TrackMetaData(BaseModel):
    """ Метаданные треков, которые мы можем получить от пользователя """
    title: str
    album_id: int
    genre_id: int # у пользователя это должно мапиться: название жанра в id, чтобы его получить
    