import httpx
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File

from src.dependencies.repository import get_artist_repository
from src.models.artist import Artist
from src.repositories.domain_repo import ArtistRepositoryABC
from src.schemas.track_meta_data import TrackMetaData
from src.domain_exceptions import *


router = APIRouter()


@router.post('/upload_track')
async def upload_track(track: UploadFile = File(...), metadata: TrackMetaData = None):
    """ Загрузка трека """

    # достать artist_id через user_id
    try:
        data = metadata.model_dump()

        async with httpx.AsyncClient() as client:
            response = await client.post(url=..., data=data)

        if response.status_code == 200:
            # тут нужно прописать логику загрузки файла в s3 или вызов этой логики
            # загружаем только после загрузки метаданных в сервис треков
            pass
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        # заменить на кастомный эксепшн
        raise HTTPException(status_code=500, detail=str(e))