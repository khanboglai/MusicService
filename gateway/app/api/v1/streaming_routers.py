from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.grpc_clients.reader_client import ReaderClient
from app.grpc_clients.streaming_client import StreamingClient
from app.api.handel_exceptions import handle_exceptions


router = APIRouter()
streaming_client = StreamingClient()
reader_client = ReaderClient()


@router.get("/stream/{track_id}")
@handle_exceptions
async def stream_file(track_id: int):
    track = await reader_client.get_track(track_id)
    album = await reader_client.get_album(track.album_id)
    file_key = f"{album.artist_id}/{track.album_id}/{track_id}.mp3"

    generator = streaming_client.stream_file(file_key)
    first_chunk = await anext(generator)

    # Оборачиваем генератор заново, начиная с уже полученного первого чанка
    async def generate():
        yield first_chunk
        async for chunk in generator:
            yield chunk

    return StreamingResponse(generate(), media_type="audio/mpeg")
