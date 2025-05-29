from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File

from src.schemas.track_meta_data import TrackCreate, AlbumCreate
from src.domain_exceptions import *
from src.grpc_client.writer_client import WriterClient

router = APIRouter()
writer_client = WriterClient()
    

@router.post("/create_track")
async def create_track(track: TrackCreate):
    try:
        track_id = await writer_client.create_track(track)
        return {"message": track_id}
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.delete("/delete_track")
async def delete_track(track_id: int):
    try:
        id = await writer_client.remove_track(track_id)
        return {"message": id}
    except NoSuchTrackException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.post("/create_album")
async def create_album(album: AlbumCreate):
    try:
        album_id = await writer_client.create_album(album)
        return {"message": album_id}
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.delete("/delete_album")
async def delete_album(album_id: int):
    try:
        id = await writer_client.remove_album(album_id)
        return {"message": id}
    except NoSuchAlbumException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))

@router.delete("/delete_albums_by_owner_id")
async def delete_albums_by_owner_id(owner_id: int):
    try:
        ids = await writer_client.remove_albums_by_owner_id(owner_id)
        return {"message": ids}
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
