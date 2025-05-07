from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File

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
        description=Description(artist.description),
        user_id=artist.user_id
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
        return {"name": artist.name,
                "email": artist.email,
                "registrations_date": artist.registered_at,
                "description": artist.description,
                "user_id": artist.user_id}
    except InvalidIdException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.delete('/delete/{user_id}')
async def delete_artist(user_id: int, artist_repo: ArtistRepositoryABC = Depends(get_artist_repository)):
    """ Удаляем исполнителя по user_id """
    try:
        artist_name = await artist_repo.delete_artist(user_id)
        return {"message": f"{artist_name} удален"}
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.get('/description/{id}')
async def get_artist_description(id: int, artist_repo: ArtistRepositoryABC = Depends(get_artist_repository)):
    """ Получаем описание исполнителя по его id """
    try:
        artist = await artist_repo.get_artist_by_id(id)
        return {"description": artist.description}
    except InvalidIdException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
