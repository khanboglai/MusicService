from datetime import date
from typing import Optional

from pydantic import BaseModel

class ArtistCreate(BaseModel):
    """ схема для создания исполнителя """
    name: str
    email: str
    registered_at: date
    cover_path: Optional[str] = None
    description: str
    user_id: int
