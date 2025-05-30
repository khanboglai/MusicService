import os

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.schemas.artist import ArtistCreate
from app.grpc_clients.artist_client import ArtistClient
from app.api.handel_exceptions import handle_exceptions, InvalidMimeType


router = APIRouter()
artist_client = ArtistClient()


@router.get('/{id}')
async def get_artist(user_id: int):
    return {"message": f"artist/{user_id}"}


# @router.get('/description/{id}')
# @handle_exceptions
# async def get_artist_description(user_id: int):
#     artist_description = await artist_client.get_description_by_user_id(user_id)
#     return {"message": f"{artist_description}"}


@router.get('/data/userid/{id}')
@handle_exceptions
async def get_artist_description_by_user_id(user_id: int):
    artist = await artist_client.get_description_by_user_id(user_id)
    return artist


@router.get('/data/{id}')
@handle_exceptions
async def get_artist_description_by_artist_id(artist_id: int):
    artist = await artist_client.get_description_by_artist_id(artist_id)
    return artist


@router.post('/create_artist', response_model=None)
@handle_exceptions
async def create_artist(artist: ArtistCreate):
    artist_id = await artist_client.create_artist(artist)
    return {"id": f"{artist_id}"}


@router.delete('/delete_artist/{id}')
@handle_exceptions
async def delete_artist(user_id: int):
    artist_user_id = await artist_client.delete_artist(user_id)
    return {"user_id": f"{artist_user_id}"}


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
