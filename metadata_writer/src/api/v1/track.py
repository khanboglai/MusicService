from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.common.database.models import Genre
from src.common.repository.abstract.album import AlbumRepositoryABC
from src.common.repository.abstract.track import TrackRepositoryABC
from src.common.dependencies.repository.album import get_album_repository
from src.common.dependencies.repository.track import get_track_repository
from src.common.models.album import Album
from src.common.models.track import Track
from src.common.schemas.album import AlbumCreate
from src.common.schemas.track import TrackCreate
from src.common.exceptions import *

router = APIRouter()

@router.post("/create", response_model=None)
async def create(track: TrackCreate, track_repo: TrackRepositoryABC = Depends(get_track_repository)):
    try:
        created_track = await track_repo.create_track(track)
        return {"message": f"{created_track.oid}"}
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

""" @router.get("/get_by_id", response_model=None)
async def get_by_id(track_id: int, track_repo: TrackRepositoryABC = Depends(get_track_repository)):
    try:
        album = await track_repo.get_track_by_id(track_id)
        return JSONResponse(album)
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    
@router.get("/get_by_album_id", response_model=None)
async def get_by_album_id(album_id: int, track_repo: TrackRepositoryABC = Depends(get_track_repository)):
    try:
        tracks = await track_repo.get_tracks_by_album_id(album_id)
        return JSONResponse(tracks)
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e)) """

@router.delete("/delete", response_model=None)
async def delete(track_id: int, track_repo: TrackRepositoryABC = Depends(get_track_repository)):
    try:
        id = await track_repo.remove_track(track_id)
        return JSONResponse({"status": "OK", "message": id})
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))