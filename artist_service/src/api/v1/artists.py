from fastapi import APIRouter, Depends, HTTPException

from src.dependencies.repository import get_artist_repository
from src.models.artist import Artist
from src.repositories.domain_repo import ArtistRepositoryABC
from src.value_objects.artist_description import Description
from src.schemas.artist import ArtistCreate
from src.domain_exceptions import *


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
    except  UniqueViolationException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.get('/{id}')
async def get_artist(id: int, artist_repo: ArtistRepositoryABC = Depends(get_artist_repository)):
    try:
        artist = await artist_repo.get_artist_by_id(id)
        return {"message": f"{artist.name}"}
    except InvalidIdException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.delete('/{id}')
async def delete_artist(id: int, artist_repo: ArtistRepositoryABC = Depends(get_artist_repository)):
    try:
        artist_name = await artist_repo.delete_artist(id)
        return {"message": f"{artist_name} удален"}
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
