import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

import redis.asyncio as redis

from src.common.core.logging import logger
from src.common.models.track import Track
from src.common.models.album import Album
from src.common.schemas.track import TrackCreate
from src.common.repository.abstract.track import TrackRepositoryABC
from src.common.exceptions import *
from src.common.database.models import Genre, track_genres_table, genres_table


class CachedTrackRepository(TrackRepositoryABC):
    """ Основной репозиторий треков (с поддержкой Redis) """

    def __init__(self, repo: TrackRepositoryABC, redis: redis.Redis):
        self.repo = repo
        self.redis = redis

    async def create_track(self, track: TrackCreate) -> Track:
        return await self.repo.create_track(track)

    async def get_track_by_id(self, id: int) -> Track:
        cache_key = f"track_{id}"
        cached = await self.redis.get(cache_key)
        if cached:
            logger.info(f"Данные о треке с {id} взяты из Redis")
            data = json.loads(cached)
            return Track(**data)

        track = await self.repo.get_artist_by_user_id(id)
        if track:
            await self.redis.setex(cache_key, 300, json.dumps(track.to_json()))
            logger.info(f"Данные о треке {track.title} записаны в Redis")

        return track

    async def get_tracks_by_album_id(self, album_id: int) -> list[Track]:
        return await self.repo.get_tracks_by_album_id(album_id)

    async def remove_track(self, track_id: int) -> int:
        return await self.repo.remove_track(track_id)
        
    async def get_track_genre(self, track_id: int):
        return await self.repo.get_track_genre(track_id)
