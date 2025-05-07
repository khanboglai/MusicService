from fastapi import APIRouter, HTTPException
from app.schemas.artist import ArtistCreate
from app.grpc_clients.artist_client import ArtistClient
from app.api.handel_exceptions import handle_exceptions


router = APIRouter()
artist_client = ArtistClient()


@router.get('/{id}')
async def get_artist(user_id: int):
    return {"message": f"artist/{user_id}"}


@router.get('/description/{id}')
@handle_exceptions
async def get_artist_description(user_id: int):
    artist_description = await artist_client.get_description(user_id)
    return {"message": f"{artist_description}"}


@router.post('/create_artist', response_model=None)
@handle_exceptions
async def create_artist(artist: ArtistCreate):
    artist_id = await artist_client.create_artist(artist)
    return {"id": f"{artist_id}"}
