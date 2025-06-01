from pydantic import BaseModel

class ArtistCreate(BaseModel):
    """ схема для создания исполнителя """
    name: str
    email: str
    description: str
    # user_id: int
