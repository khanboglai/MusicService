""" схемы для исполнителя """

from pydantic import BaseModel
from datetime import date

class ArtistCreate(BaseModel):
    """ схема для создания исполнителя """
    name: str
    email: str
    registered_at: date
    description: str
    user_id: int
