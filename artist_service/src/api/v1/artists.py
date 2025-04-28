import datetime
from http.client import HTTPResponse

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.artist import Artist
from src.repositories.artist_repo import ArtistRepository
from src.database.postgres import get_session
from src.value_objects.artist_description import Description
from src.schemas.artist import ArtistCreate


router = APIRouter()

@router.post('/create', response_model=None)
async def create_artist(artist: ArtistCreate, db: AsyncSession = Depends(get_session)):

    artist_repo = ArtistRepository(db)

    new_artist = Artist(
        name=artist.name,
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
async def get_artist(id: int, db: AsyncSession = Depends(get_session)):
    artist_repo = ArtistRepository(db)
    try:
        artist = await artist_repo.get_artist(id)
        return {"message": f"{artist.name}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))