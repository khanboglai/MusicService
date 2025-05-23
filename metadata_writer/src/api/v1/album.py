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
async def create(album: AlbumCreate, album_repo: AlbumRepositoryABC = Depends(get_album_repository)):
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

""" @router.get("/get_by_id", response_model=None)
async def get_by_id(album_id: int, album_repo: AlbumRepositoryABC = Depends(get_album_repository)):
    try:
        album = await album_repo.get_album_by_id(album_id)
        return JSONResponse(album)
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.get("/get_by_owner_id", response_model=None)
async def get_by_owner_id(owner_id: int, album_repo: AlbumRepositoryABC = Depends(get_album_repository)):
    albums = await album_repo.get_albums_by_owner_id(owner_id)
    return JSONResponse(albums) """

@router.delete("/delete", response_model=None)
async def delete(album_id: int, album_repo: AlbumRepositoryABC = Depends(get_album_repository)):
    try:
        id = await album_repo.remove_album(album_id)
        return JSONResponse({"status": "OK", "message": id})
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.delete("/delete_by_owner_id", response_model=None)
async def delete_by_owner_id(owner_id: int, album_repo: AlbumRepositoryABC = Depends(get_album_repository)):
    try:
        ids = await album_repo.remove_albums_by_owner_id(owner_id)
        return JSONResponse({
            "status": "OK",
            "message": ids
        })
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e)) 
