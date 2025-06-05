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


@router.get("/get_by_id", response_model=None)
async def get_by_id(track_id: int, track_repo: TrackRepositoryABC = Depends(get_track_repository)):
    """ API ручка для получения информации о треке по его ID"""
    try:
        track = await track_repo.get_track_by_id(track_id)
        return JSONResponse(track.to_json())
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    
@router.get("/get_by_album_id", response_model=None)
async def get_by_album_id(album_id: int, track_repo: TrackRepositoryABC = Depends(get_track_repository)):
    """ API ручка для получения списка треков из альбома по ID альбома """
    try:
        tracks = await track_repo.get_tracks_by_album_id(album_id)
        json_tracks = []
        for track in tracks:
            json_tracks.append(track.to_json())
        return JSONResponse(json_tracks)
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))