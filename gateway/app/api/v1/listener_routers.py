import os

from fastapi import APIRouter, HTTPException
# from app.schemas.artist import ArtistCreate
from app.grpc_clients.listener_client import ListenerClient
from app.api.handel_exceptions import handle_exceptions, InvalidMimeType


router = APIRouter()
listener_client = ListenerClient()


# @router.get('/{id}')
# async def get_artist(user_id: int):
#     return {"message": f"artist/{user_id}"}


@router.get('/listeners/{listener_id}')
@handle_exceptions
async def get_artist_description(listener_id: int):
    listener = await listener_client.get_listener(listener_id)
    return {"message": f"{listener}"}


# @router.post('/create_artist', response_model=None)
# @handle_exceptions
# async def create_artist(artist: ArtistCreate):
#     artist_id = await artist_client.create_artist(artist)
#     return {"id": f"{artist_id}"}


# @router.post('/upload_cover')
# @handle_exceptions
# async def upload_cover(file: UploadFile = File(...), user_id: int = Form(...)):

#     # должен быть метод для извлечения user_id из jwt

#     if not file.content_type.startswith('image/jpeg'):
#         raise InvalidMimeType("Неверный формат файла")

#     temp_file = f"temp_{file.filename}"
#     with open(temp_file, "wb") as f:
#         content = await file.read()
#         f.write(content)

#     response = await artist_client.upload_cover(temp_file, user_id)
#     os.remove(temp_file)
#     return {"message": response.message}
