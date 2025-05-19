from fastapi import APIRouter, Depends, HTTPException

from src.common.database.models import Genre
from src.common.repository.abstract.album import AlbumRepositoryABC
from src.common.repository.abstract.track import TrackRepositoryABC
from src.common.dependencies.repository import get_album_repository, get_track_repository
from src.common.models.album import Album
from src.common.models.track import Track
from src.common.schemas.album import AlbumCreate
from src.common.schemas.track import TrackCreate
from src.common.exceptions import *


router = APIRouter(prefix="/api/v1")

@router.post("/create_album", response_model=None)
async def create_album(album: AlbumCreate, album_repo: AlbumRepositoryABC = Depends(get_album_repository)):
    new_album = Album(
        title=album.title,
        owner_id=album.owner_id,
        release_date=album.release_date,
    )

    try:
        created_album = await album_repo.create_album(new_album)
        return {"message": f"{created_album.oid}"}
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.post("/create_track", response_model=None)
async def create_track(track: TrackCreate, track_repo: TrackRepositoryABC = Depends(get_track_repository)):
    try:
        created_track = await track_repo.create_track(track)
        return {"message": f"{created_track.oid}"}
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
