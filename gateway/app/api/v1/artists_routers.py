from fastapi import APIRouter, HTTPException
from pydantic.v1 import NoneStr

from app.schemas.artist import ArtistCreate
from app.grpc_clients.artist_client import ArtistClient

router = APIRouter()
artist_client = ArtistClient()

@router.get('/{id}')
async def get_artist(user_id: int):
    return {"message": f"artist/{user_id}"}

@router.get('/description/{id}')
async def get_artist_description(user_id: int):
    return {"message": f"description/{user_id}"}

@router.post('/create_artist', response_model=None)
async def create_artist(artist: ArtistCreate):
    try:
        artist_id = artist_client.create_artist(artist.name, artist.description)
        return {"id": f"{artist_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # return {"message": f"artist/{artist.user_id}"}