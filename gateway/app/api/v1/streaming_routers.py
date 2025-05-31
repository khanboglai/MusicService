import grpc
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.grpc_clients.streaming_client import StreamingClient
from app.domain_exceptions.streaming_exceptions import StreamingException


router = APIRouter()
streaming_client = StreamingClient()


@router.get("/stream/{artist_id}/{album_id}/{track_id}")
async def stream_file(artist_id: str, album_id: str, track_id: str):
    file_key = f"{artist_id}/{album_id}/{track_id}.mp3"

    # Предварительная проверка: получаем первый chunk до начала отправки ответа
    try:
        generator = streaming_client.stream_file(file_key)
        first_chunk = await anext(generator)

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"file not found {file_key}")
    except StreamingException as e:
        raise HTTPException(status_code=500, detail=f"Streaming error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    # Оборачиваем генератор заново, начиная с уже полученного первого чанка
    async def generate():
        yield first_chunk
        async for chunk in generator:
            yield chunk

    return StreamingResponse(generate(), media_type="audio/mpeg")
