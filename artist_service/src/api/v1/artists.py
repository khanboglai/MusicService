from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.dependencies.repository import get_artist_repository
from src.models.artist import Artist
from src.repositories.domain_repo import ArtistRepositoryABC
from src.value_objects.artist_description import Description
from src.schemas.artist import ArtistCreate


router = APIRouter()

@router.post('/create', response_model=None)
async def create_artist(artist: ArtistCreate, artist_repo: ArtistRepositoryABC = Depends(get_artist_repository)):

    new_artist = Artist(
        name=artist.name,
        email=artist.email,
        registered_at=artist.registered_at,
        cover_path=artist.cover_path,
        description=Description(artist.description),
    )

    try:
        created_artist = await artist_repo.create_artist(new_artist)
        return {"message": f"{created_artist.name}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{id}')
async def get_artist(id: int, artist_repo: ArtistRepositoryABC = Depends(get_artist_repository)):
    try:
        artist = await artist_repo.get_artist_by_id(id)
        return {"message": f"{artist.name}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
