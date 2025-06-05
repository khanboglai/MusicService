import json
from typing import Optional

from src.models.artist import Artist
from src.repositories.domain_repo import ArtistRepositoryABC
import redis.asyncio as redis
from src.core.logging import logger


class CachedArtistRepo(ArtistRepositoryABC):
    def __init__(self, repo: ArtistRepositoryABC, redis: redis.Redis) -> None:
        self.repo = repo
        self.redis = redis

    async def create_artist(self, artist: Artist) -> Artist:
        """ Функция для создания исполнителя """
        return await self.repo.create_artist(artist)

    async def get_artist_by_id(self, artist_id: int) -> Artist:
        """ Функция для получения данных исполнителя по id """
        cache_key = f"artist_loc_{artist_id}"
        cached = await self.redis.get(cache_key)
        if cached:
            logger.info(f"Данные об исполнителе с id {artist_id} взяты из Redis")
            data = json.loads(cached)
            return Artist.from_dict(data)

        artist = await self.repo.get_artist_by_id(artist_id)
        if artist:
            await self.redis.setex(cache_key, 300, json.dumps(artist.to_dict()))
            logger.info(f"Данные об исполнителе {artist.name} записаны в Redis")

        return artist

    async def get_artist_by_user_id(self, user_id: int) -> Optional[Artist]:
        """ Функция для получения данных исполнителя по user_id """
        cache_key = f"artist_{user_id}"
        cached = await self.redis.get(cache_key)
        if cached:
            logger.info(f"Данные об исполнителе с user_id {user_id} взяты из Redis")
            data = json.loads(cached)
            return Artist.from_dict(data)

        artist = await self.repo.get_artist_by_user_id(user_id)
        if artist:
            await self.redis.setex(cache_key, 300, json.dumps(artist.to_dict()))
            logger.info(f"Данные об исполнителе {artist.name} записаны в Redis")

        return artist

    async def delete_artist(self, user_id: int):
        """ Функция для удаления исполнителя """
        return await self.repo.delete_artist(user_id=user_id)
