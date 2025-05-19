import os

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.schemas.artist import ArtistCreate
from app.grpc_clients.artist_client import ArtistClient
from app.api.handel_exceptions import handle_exceptions


router = APIRouter()
artist_client = ArtistClient()


@router.get('/{id}')
async def get_artist(user_id: int):
    return {"message": f"artist/{user_id}"}


@router.get('/description/{id}')
@handle_exceptions
async def get_artist_description(user_id: int):
    artist_description = await artist_client.get_description(user_id)
    return {"message": f"{artist_description}"}


@router.post('/create_artist', response_model=None)
@handle_exceptions
async def create_artist(artist: ArtistCreate):
    artist_id = await artist_client.create_artist(artist)
    return {"id": f"{artist_id}"}


@router.post('/upload_cover')
async def upload_cover(file: UploadFile = File(...), user_id: int = Form(...)):

    # должен быть метод для извлечения user_id из jwt

    if not file.content_type.startswith('image/jpeg'):
        raise HTTPException(status_code=400, detail="Invalid file type")

    try:
        temp_file = f"temp_{file.filename}"
        with open(temp_file, "wb") as f:
            content = await file.read()
            f.write(content)

        response = await artist_client.upload_cover(temp_file, user_id)

        os.remove(temp_file)
        return {"message": response.message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
