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
async def get_by_id(album_id: int, album_repo: AlbumRepositoryABC = Depends(get_album_repository)):
    """ API ручка для получения информации об альбоме по его ID """
    try:
        album = await album_repo.get_album_by_id(album_id)
        return JSONResponse(album.to_json())
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.get("/get_by_owner_id", response_model=None)
async def get_by_owner_id(owner_id: int, album_repo: AlbumRepositoryABC = Depends(get_album_repository)):
    """ API ручка для получения списка альбомов по ID автора """
    albums = await album_repo.get_albums_by_owner_id(owner_id)
    json_albums = []
    for album in albums:
        json_albums.append(album.to_json())
    return JSONResponse(json_albums)
