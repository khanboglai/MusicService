from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.grpc_clients.streaming_client import StreamingClient


router = APIRouter()
streaming_client = StreamingClient()


@router.get("/stream/{artist_id}/{album_id}/{track_id}")
async def stream_file(artist_id: str, album_id: str, track_id: str):
    try:
        # Вызываем метод gRPC-клиента
        file_key = f"{artist_id}/{album_id}/{track_id}.mp3"
        responses = await streaming_client.stream_file(file_key)

        # Генератор для потоковой передачи данных
        async def generate():
            async for response in responses:
                yield response.data

        # Возвращаем потоковый ответ
        return StreamingResponse(generate(), media_type="audio/mpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error streaming file: {str(e)}")
