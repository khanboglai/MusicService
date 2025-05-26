""" Ручки клиента слушателя """
import os

from fastapi import APIRouter, HTTPException
from app.grpc_clients.listener_client import ListenerClient
from app.grpc_clients.reader_client import ReaderClient
from app.api.handel_exceptions import handle_exceptions, InvalidMimeType


router = APIRouter()
listener_client = ListenerClient()
reader_client = ReaderClient()


@router.get('/listener/get')
@handle_exceptions
async def read_listener(user_id: int):
    listener = await listener_client.get_listener(user_id)
    return {
        "listener_id": int(listener.listener_id),
        "user_id": int(listener.user_id),
        "first_name": str(listener.first_name),
        "last_name": str(listener.last_name)
    }

@router.post('/listener/add')
@handle_exceptions
async def add_listener(
        user_id: int, # временно, потом будем получать из куки
        first_name: str,
        last_name: str,
        birth_date: str,
    ):
    listener = await listener_client.create_listener(
            user_id,
            first_name,
            last_name,
            birth_date,
        )
    return {
        "listener_id": int(listener.listener_id),
        "user_id": int(listener.user_id),
        "first_name": str(listener.first_name),
        "last_name": str(listener.last_name)
    }

@router.delete('/listener/delete')
@handle_exceptions
async def erase_listener(user_id: int):
    message = await listener_client.delete_listener(user_id)
    return {
        "message": str(message.delete_message)
    }

@router.post('/like')
@handle_exceptions
async def liking(user_id: int, track_id: int):
    like = await listener_client.like(user_id, track_id)
    if not like.HasField("deleted"):
        return {
            "like": {
                "like_id": int(like.liked.id),
                "track_id": int(like.liked.track_id),
                "listener": {
                    "listener_id": int(like.liked.listener.listener_id),
                    "user_id": int(like.liked.listener.user_id),
                    "first_name": str(like.liked.listener.first_name),
                    "last_name": str(like.liked.listener.last_name),
                    "birthdate": str(like.liked.listener.birth_date)
                }
            }
        }
    return {"message": "Like deleted successfully!"}

@router.post('/interaction')
@handle_exceptions
async def interacting(
        user_id: int, # временно
        track_id: int, # это останется здесь (тк на фронте когда мы нажимаем на кнопку трека, то с фронта на бэк идет айдишник)
        # track_name: str, # перенесется в тело функции (запрос к сервису ридера)
        listen_time: int,
        # artist_id: int, # перенесется в тело функции (запрос к сервису ридера)
        artist_name: str, # перенесется в тело функции (запрос к сервису артиста)
        # genre_id: int, # перенесется в тело функции (запрос к сервису ридера)
        # genre_name: str, # перенесется в тело функции (запрос к сервису ридера)
    ):
    track_info = await reader_client.get_track(track_id)
    album_info = await reader_client.get_album(int(track_info.album_id))
    genre_info = await reader_client.get_track_genre(track_id)
    interaction = await listener_client.interaction(user_id, track_id, listen_time, str(track_info.title), int(album_info.artist_id), artist_name, int(genre_info.genre_id), str(genre_info.genre_name))
    return {
        "track_id": int(interaction.track_id),
        "listen_time": int(interaction.listen_time),
        "listener": {
            "listener_id": int(interaction.listener.listener_id),
            "user_id": int(interaction.listener.user_id),
            "first_name": str(interaction.listener.first_name),
            "last_name": str(interaction.listener.last_name),
            "birthdate": str(interaction.listener.birth_date)
        }
    }

@router.get('/history')
@handle_exceptions
async def load_history(user_id: int):
    history = await listener_client.history(user_id)
    for interaction in history.interactions:
        print(f"{interaction.track_id} {interaction.last_interaction}")
    return {
        "listener": {
            "listener_id": int(history.listener.listener_id),
            "user_id": int(history.listener.user_id),
            "first_name": str(history.listener.first_name),
            "last_name": str(history.listener.last_name),
            "birthdate": str(history.listener.birth_date)
        },
        "history": [
            {"track_id": interaction.track_id, "last_interaction": interaction.last_interaction} for interaction in history.interactions
        ]
    }
