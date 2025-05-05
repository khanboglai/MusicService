""" схемы для исполнителя """

from pydantic import BaseModel
from typing import Optional
from datetime import date

class ArtistCreate(BaseModel):
    """ схема для создания исполнителя """
    name: str
    email: str
    registered_at: date
    cover_path: Optional[str] = None
    description: str
    user_id: int
