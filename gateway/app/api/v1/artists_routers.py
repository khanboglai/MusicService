import os
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Request, Response
from app.schemas.artist import ArtistCreate
from app.grpc_clients.artist_client import ArtistClient
from app.grpc_clients.auth_client import AuthClient
from app.grpc_clients.writer_client import WriterClient
from app.api.handel_exceptions import handle_exceptions, InvalidMimeType
from app.schemas.track_meta_data import TrackCreate, AlbumCreate
from app.domain_exceptions import *


router = APIRouter()
artist_client = ArtistClient()
auth_client = AuthClient()
writer_client = WriterClient()


@router.get('/data/userid/')
@handle_exceptions
async def get_artist_description_by_user_id(request: Request, response: Response):
    access_token = request.cookies.get('access_token')
    refresh_token = request.cookies.get('refresh_token')

    if access_token is None:
        access_token = ""
    if refresh_token is None:
        refresh_token = ""

    user = await auth_client.get_me(access_token, refresh_token)
    artist = await artist_client.get_description_by_user_id(user.user_id)

    response.set_cookie(
        key="access_token",
        value=str(user.access_token),
        httponly=True,
    )

    return artist


@router.get('/data/{id}')
@handle_exceptions
async def get_artist_description_by_artist_id(artist_id: int):
    artist = await artist_client.get_description_by_artist_id(artist_id)
    return artist


@router.post('/create_artist', response_model=None)
@handle_exceptions
async def create_artist(artist: ArtistCreate, request: Request, response: Response):
    access_token = request.cookies.get('access_token')
    refresh_token = request.cookies.get('refresh_token')

    if access_token is None:
        access_token = ""
    if refresh_token is None:
        refresh_token = ""

    user = await auth_client.get_me(access_token, refresh_token)
    artist_id = await artist_client.create_artist(artist, user.user_id)

    response.set_cookie(
        key="access_token",
        value=str(user.access_token),
        httponly=True,
    )

    return {"id": f"{artist_id}"}


@router.delete('/delete_artist/')
@handle_exceptions
async def delete_artist(request: Request, response: Response):
    access_token = request.cookies.get('access_token')
    refresh_token = request.cookies.get('refresh_token')

    if access_token is None:
        access_token = ""
    if refresh_token is None:
        refresh_token = ""

    user = await auth_client.get_me(access_token, refresh_token)
    artist_user_id = await artist_client.delete_artist(user.user_id)

    response.set_cookie(
        key="access_token",
        value=str(user.access_token),
        httponly=True,
    )

    return {"user_id": f"{artist_user_id}"}


@router.get("/artist_id/{id}")
@handle_exceptions
async def get_artist_id(user_id: int, request: Request, response: Response):
    id = await artist_client.get_artist_id(user_id)
    return id


# @router.post('/upload_cover')
# @handle_exceptions
# async def upload_cover(file: UploadFile = File(...), user_id: int = Form(...)):
#
#     # должен быть метод для извлечения user_id из jwt
#
#     if not file.content_type.startswith('image/jpeg'):
#         raise InvalidMimeType("Неверный формат файла")
#
#     temp_file = f"temp_{file.filename}"
#     with open(temp_file, "wb") as f:
#         content = await file.read()
#         f.write(content)
#
#     response = await artist_client.upload_cover(temp_file, user_id)
#     os.remove(temp_file)
#     return {"message": response.message}



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
async def create_album(album: AlbumCreate, request: Request, response: Response):
    try:
        access_token = request.cookies.get('access_token')
        refresh_token = request.cookies.get('refresh_token')

        if access_token is None:
            access_token = ""
        if refresh_token is None:
            refresh_token = ""

        user = await auth_client.get_me(access_token, refresh_token)
        artist_id = await artist_client.get_artist_id(user.user_id)
        album_id = await writer_client.create_album(album, artist_id)

        response.set_cookie(
            key="access_token",
            value=str(user.access_token),
            httponly=True,
        )

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
async def delete_albums_by_owner_id(request: Request, response: Response):
    try:
        access_token = request.cookies.get('access_token')
        refresh_token = request.cookies.get('refresh_token')

        if access_token is None:
            access_token = ""
        if refresh_token is None:
            refresh_token = ""

        user = await auth_client.get_me(access_token, refresh_token)
        owner_id = await artist_client.get_artist_id(user.user_id)
        ids = await writer_client.remove_albums_by_owner_id(owner_id)

        response.set_cookie(
            key="access_token",
            value=str(user.access_token),
            httponly=True,
        )

        return {"message": ids}
    except DatabaseException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
