""" Ручки клиента слушателя """
import os

from fastapi import APIRouter, HTTPException, Depends
from app.grpc_clients.listener_client import ListenerClient
from app.grpc_clients.reader_client import ReaderClient
from app.grpc_clients.artist_client import ArtistClient
from app.api.handel_exceptions import handle_exceptions, InvalidMimeType
from app.search import search_for
from app.api.v1.auth_routers import check_role
from app.schemas.role_enum import RoleEnum


router = APIRouter()
# подключаем клиентов других сервисов
listener_client = ListenerClient()
reader_client = ReaderClient()
artist_client = ArtistClient()


@router.get('/listener/get')
@handle_exceptions
async def read_listener(user = Depends(check_role(RoleEnum.LISTNER.value))):
    listener = await listener_client.get_listener(user.user_id)
    return {
        "listener_id": int(listener.listener_id),
        "user_id": int(listener.user_id),
        "first_name": str(listener.first_name),
        "last_name": str(listener.last_name)
    }

@router.post('/listener/add')
@handle_exceptions
async def add_listener(
        first_name: str,
        last_name: str,
        birth_date: str,
        user = Depends(check_role(RoleEnum.LISTNER.value)),
    ):
    listener = await listener_client.create_listener(
            user.user_id,
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
async def erase_listener(user = Depends(check_role(RoleEnum.LISTNER.value))):
    message = await listener_client.delete_listener(user.user_id)
    return {
        "message": str(message.delete_message)
    }

@router.get('/albums')
@handle_exceptions
async def get_all_albums(user = Depends(check_role(RoleEnum.LISTNER.value))):
    albums = await reader_client.get_all_albums()
    return {
        "albums": [
            {
                "album_id": int(album.album_id),
                "title": str(album.title),
                "artist_id": int(album.artist_id),
                "release_date": str(album.release_date)
            }
            for album in albums.albums
        ]  
    }

@router.get('/album/{album_id}')
@handle_exceptions
async def get_tracks_in_album(album_id: int, user = Depends(check_role(RoleEnum.LISTNER.value))):
    tracks = await reader_client.get_tracks_in_album(album_id)
    return {
        "tracks": [
            {
                "track_id": track.track_id,
                "title": track.title,
                "album_id": track.album_id,
            }
            for track in tracks.tracks
        ]
    }

@router.get('/artist/{artist_id}')
@handle_exceptions
async def get_albums_in_artist(artist_id: int, user = Depends(check_role(RoleEnum.LISTNER.value))):
    albums = await reader_client.get_albums_in_artist(artist_id)
    return {
        "albums": [
            {
                "album_id": int(album.album_id),
                "title": str(album.title),
                "artist_id": int(album.artist_id), # возможно надо будет достать еще и имя артиста
                "release_date": str(album.release_date)
            }
            for album in albums.albums
        ]     
    }

@router.get('/tracks/{track_id}')
@handle_exceptions
async def get_track_info(track_id: int, user = Depends(check_role(RoleEnum.LISTNER.value))):
    track = await reader_client.get_track(track_id)
    return {
        "track_id": track.track_id,
        "title": track.title,
        "album_id": track.album_id,
    }

@router.post('/like')
@handle_exceptions
async def liking(track_id: int, user = Depends(check_role(RoleEnum.LISTNER.value))):
    like = await listener_client.like(user.user_id, track_id)
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
        track_id: int, # это останется здесь (тк на фронте когда мы нажимаем на кнопку трека, то с фронта на бэк идет айдишник)
        listen_time: int,
        user = Depends(check_role(RoleEnum.LISTNER.value))
    ):
    track_info = await reader_client.get_track(track_id)
    album_info = await reader_client.get_album(int(track_info.album_id))
    genre_info = await reader_client.get_track_genre(track_id)
    artist_name = (await artist_client.get_data_by_artist_id(int(album_info.artist_id)))[1]
    interaction = await listener_client.interaction(
        user.user_id,
        track_id,
        listen_time,
        str(track_info.title),
        int(album_info.artist_id),
        artist_name,
        int(genre_info.genre_id),
        str(genre_info.genre_name)
    )

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
async def load_history(user = Depends(check_role(RoleEnum.LISTNER.value))):
    history = await listener_client.history(user.user_id)
    tracks_in_history = []
    for interaction in history.interactions:
        track_info = await reader_client.get_track(interaction.track_id)
        tracks_in_history.append({"track_id": interaction.track_id, "title": track_info.title, "last_interaction": interaction.last_interaction})
    return {
        "listener": {
            "listener_id": int(history.listener.listener_id),
            "user_id": int(history.listener.user_id),
            "first_name": str(history.listener.first_name),
            "last_name": str(history.listener.last_name),
            "birthdate": str(history.listener.birth_date)
        },
        "history": tracks_in_history
    }

@router.post('/playlist/create')
@handle_exceptions
async def create_playlist(title: str, user = Depends(check_role(RoleEnum.LISTNER.value))):
    playlist = await listener_client.create_playlist(user.user_id, title)
    return {
        "playlist_id": int(playlist.playlist_id),
        "title": str(playlist.title),
    }

@router.delete('/playlists/delete')
@handle_exceptions
async def delete_playlist(playlist_id: int, user = Depends(check_role(RoleEnum.LISTNER.value))):
    message = await listener_client.delete_playlist(user.user_id, playlist_id)
    return {
        "message": str(message.delete_message)
    }

@router.get('/playlists')
@handle_exceptions
async def get_all_playlists(user = Depends(check_role(RoleEnum.LISTNER.value))):
    playlists = await listener_client.get_all_playlists(user.user_id)
    return {
        "listener": {
        "listener_id": int(playlists.listener.listener_id),
        "user_id": int(playlists.listener.user_id),
        "first_name": str(playlists.listener.first_name),
        "last_name": str(playlists.listener.last_name),
        "birthdate": str(playlists.listener.birth_date)
        },
        "playlists": [
            {
                "playlist_id": int(playlist.playlist_id),
                "title": str(playlist.title),
            }
            for playlist in playlists.playlists
        ]
    }


@router.post('/playlists/{playlist_id}/add_track')
@handle_exceptions
async def add_new_track_in_playlist(playlist_id: int, track_id: int, user = Depends(check_role(RoleEnum.LISTNER.value))):
    track = await listener_client.add_new_track_in_playlist(user.user_id, playlist_id, track_id)
    track_info = await reader_client.get_track(track_id)
    return {
        "playlist_id": int(track.playlist_id),
        "track_id": int(track_info.track_id),
        "track_title": str(track_info.title),
    }


@router.delete('/playlists/{playlist_id}/delete_track')
@handle_exceptions
async def delete_track_from_playlist(playlist_id: int, track_id: int, user = Depends(check_role(RoleEnum.LISTNER.value))):
    message = await listener_client.delete_track_from_playlist(user.user_id, playlist_id, track_id)
    return {
        "message": str(message.delete_message),
    }

@router.get('/playlists/{playlist_id}/tracks')
@handle_exceptions
async def get_all_tracks_in_playlist(playlist_id: int, user = Depends(check_role(RoleEnum.LISTNER.value))):
    tracks = await listener_client.get_all_tracks_in_playlist(user.user_id, playlist_id)
    tracks_in_playlist = []
    for track in tracks.tracks:
        track_info = await reader_client.get_track(track.track_id)
        tracks_in_playlist.append({"track_id": int(track.track_id), "track_title": str(track_info.title)})
    return {
        "playlist": tracks_in_playlist,
    }


@router.get("/search/albums/{query}/page={page}")
@handle_exceptions
async def search_albums(query: str, page: int, user = Depends(check_role(RoleEnum.LISTNER.value))):
    r = await search_for("albums", query, page)

    result = []
    for hit in r:
        album = await reader_client.get_album(int(hit["_id"]))
        result.append({
            "album_id": album.album_id,
            "title": album.title,
            "owner_id": album.artist_id,
            "release_date": album.release_date
        })
    return result


@router.get("/search/tracks/{query}/page={page}")
@handle_exceptions
async def search_tracks(query: str, page: int, user = Depends(check_role(RoleEnum.LISTNER.value))):
    r = await search_for("tracks", query, page)

    result = []
    for hit in r:
        track = await reader_client.get_track(int(hit["_id"]))
        result.append({
            "track_id": track.track_id,
            "title": track.title,
            "album_id": track.album_id,
            "explicit": track.explicit
        })
    return result

@router.get("/search/artists/{query}/page={page}")
@handle_exceptions
async def search_artists(query: str, page: int):
    r = await search_for("artists", query, page)

    result = []
    for hit in r:
        artist = await artist_client.get_data_by_artist_id(int(hit["_id"]))
        result.append({
            "artist_id": artist[0],
            "name": artist[1],
            "description": artist[2],
            "registered_at" : artist[3]
        })
    return result
