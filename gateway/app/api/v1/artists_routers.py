import json
import os
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Request, Response, Depends
from botocore.exceptions import ClientError, NoCredentialsError
from app.schemas.artist import ArtistCreate
from app.grpc_clients.artist_client import ArtistClient
from app.grpc_clients.auth_client import AuthClient
from app.grpc_clients.writer_client import WriterClient
from app.api.handel_exceptions import handle_exceptions, InvalidMimeType
from app.schemas.track_meta_data import TrackCreate, AlbumCreate
from app.domain_exceptions import *
from app.api.v1.auth_routers import check_role
from app.schemas.role_enum import RoleEnum
from app.core.config import settings
from app.core.logging import logger


router = APIRouter()
artist_client = ArtistClient()
auth_client = AuthClient()
writer_client = WriterClient()


@router.get('/data/userid/')
@handle_exceptions
async def get_artist_data_by_user_id(user = Depends(check_role(RoleEnum.ARTIST.value))):
    """ ручка для получения описания пользователя """
    artist = await artist_client.get_data_by_user_id(user.user_id)
    return artist


@router.get('/data/{id}')
@handle_exceptions
async def get_artist_data_by_artist_id(artist_id: int, user = Depends(check_role(RoleEnum.ARTIST.value))):
    artist = await artist_client.get_data_by_artist_id(artist_id)
    return artist


@router.post('/create_artist')
@handle_exceptions
async def create_artist(artist: ArtistCreate, user = Depends(check_role(RoleEnum.ARTIST.value))):
    """ Ручка для создания исполнителя """
    artist_id = await artist_client.create_artist(artist, user.user_id)
    return {"id": f"{artist_id}"}


@router.delete('/delete_artist/')
@handle_exceptions
async def delete_artist(user = Depends(check_role(RoleEnum.ARTIST.value))):
    """ Ручка для удаления исполнителя """
    artist_user_id = await artist_client.delete_artist(user.user_id)
    return {"user_id": f"{artist_user_id}"}


@router.get("/artist_id/")
@handle_exceptions
async def get_artist_id(user = Depends(check_role(RoleEnum.ARTIST.value))):
    """ Ручка для получения artist_id по user_id """
    id = await artist_client.get_artist_id(user.user_id)
    return id


@router.post("/create_track")
async def create_track(track_data: str = Form(...), file: UploadFile = File(...), user = Depends(check_role(RoleEnum.ARTIST.value))):
    """ Ручка для создания трека """
    track_id = None
    try:
        track = TrackCreate(**json.loads(track_data))
        track_id = await writer_client.create_track(track)

        if not file.content_type.startswith('audio/mpeg'):
            # удаляем данные трека, в случае проблем
            id = await writer_client.remove_track(track_id)
            raise InvalidMimeType("Неверный формат файла")

        # инициализация подключения к minio
        s3_client = settings.create_minio_client()
        settings.create_bucket_if_not_exists(s3_client)
        bucket_name = settings.minio_bucket_name

        # формирование пути для загрузки файлов
        artist_id = await artist_client.get_artist_id(user.user_id)
        album_id = track.album_id
        file_path = f"/{artist_id}/{album_id}/{track_id}.mp3"

        status = settings.upload_file_to_s3(file.file, bucket_name, file_path, s3_client)
        return {"message": track_id, "file_upload_status": status}
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except (ClientError, NoCredentialsError) as e:
        logger.error(f"Failed to upload file: {e}")
        id = await writer_client.remove_track(track_id)
        raise HTTPException(status_code=500, detail="Внутрення ошибка")


@router.delete("/delete_track")
async def delete_track(track_id: int, user = Depends(check_role(RoleEnum.ARTIST.value))):
    """ Ручка для удаления трека """
    try:
        id = await writer_client.remove_track(track_id)
        return {"message": id}
    except NoSuchTrackException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.post("/create_album")
async def create_album(album: AlbumCreate, user = Depends(check_role(RoleEnum.ARTIST.value))):
    """ Ручка для создания альбома """
    try:
        artist_id = await artist_client.get_artist_id(user.user_id)
        album_id = await writer_client.create_album(album, artist_id)

        return {"message": album_id}
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.delete("/delete_album")
async def delete_album(album_id: int, user = Depends(check_role(RoleEnum.ARTIST.value))):
    """ Ручка для удаления альбома """
    try:
        id = await writer_client.remove_album(album_id)
        return {"message": id}
    except NoSuchAlbumException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.delete("/delete_albums_by_owner_id")
async def delete_albums_by_owner_id(user = Depends(check_role(RoleEnum.ARTIST.value))):
    """ Ручка для удаления альбома по artist_id """
    try:
        owner_id = await artist_client.get_artist_id(user.user_id)
        ids = await writer_client.remove_albums_by_owner_id(owner_id)

        return {"message": ids}
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
