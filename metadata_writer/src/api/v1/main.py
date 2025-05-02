import datetime
from http.client import HTTPResponse

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.track import Track
from src.models.album import Album
from src.repository.album import AlbumRepository
from src.repository.track import TrackRepository
from src.database.session import get_session

from src.schemas.metadata import AlbumCreate, TrackCreate

router = APIRouter()

@router.post("/create_album", response_model=None)
async def create_album(album: AlbumCreate, db: AsyncSession = Depends(get_session)):
    repo = AlbumRepository(db)

    new_album = Album(
        title=album.title,
        cover_path=album.cover_path,
        release_date=album.release_date,
        author_id=album.author_id
    )

    try:
        created_artist = await repo.create_artist(new_album)
        return {"message": f"{created_artist.title}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create_track", response_model=None)
async def create_track(track: TrackCreate, db: AsyncSession = Depends(get_session)):
    repo = TrackRepository(db)

    new_track = Track(
        title=track.title,
        album_id=track.album_id,
        file_path=track.file_path,
        explicit=track.explicit,
    )

    try:
        created_artist = await repo.create_artist(new_track)
        return {"message": f"{created_artist.title}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))