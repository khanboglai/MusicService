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
from src.common.search import add_album_to_es, rmv_album_from_es, rmv_track_from_es

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
        r = await add_album_to_es(album_id=created_album.oid, title=album.title)
        return {"message": f"{created_album.oid}"}
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.delete("/delete", response_model=None)
async def delete(album_id: int, album_repo: AlbumRepositoryABC = Depends(get_album_repository), track_repo: TrackRepositoryABC = Depends(get_track_repository)):
    try:
        tids = [track.track_id for track in track_repo.get_tracks_by_album_id(album_id)]

        id = await album_repo.remove_album(album_id)
        r = await rmv_album_from_es(album_id=id)

        for tid in tids:
            r = await rmv_track_from_es(tid)
        return JSONResponse({"status": "OK", "message": id})
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.delete("/delete_by_owner_id", response_model=None)
async def delete_by_owner_id(owner_id: int, album_repo: AlbumRepositoryABC = Depends(get_album_repository), track_repo: TrackRepositoryABC = Depends(get_track_repository)):
    try:
        ids = await album_repo.remove_albums_by_owner_id(owner_id)
        for id in ids:
            tids = [track.track_id for track in track_repo.get_tracks_by_album_id(id)]
            r = await rmv_album_from_es(album_id=id)
            for tid in tids:
                r = await rmv_track_from_es(tid)
        return JSONResponse({
            "status": "OK",
            "message": ids
        })
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e)) 
