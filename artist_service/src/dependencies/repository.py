""" Тут зависимости для слоя репозитория """
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.postgres import get_session
from src.repositories.artist_repo import ArtistRepository
from src.repositories.domain_repo import ArtistRepositoryABC
from src.repositories.cache_artist_repo import CachedArtistRepo


def get_artist_repository(db: AsyncSession = Depends(get_session)) -> ArtistRepositoryABC:
    """
    Функция для возврата нужного репозитория
    Здесь надо будет прописать репозиторий, который работает с кешированием
    """
    return ArtistRepository(db)


class ArtistRepositoryFactory:
    @staticmethod
    async def create(db: AsyncSession = Depends(get_session), use_cache: bool = False, redis_client=None) -> ArtistRepositoryABC:
        repo = ArtistRepository(db)
        if use_cache and redis_client:
            return CachedArtistRepo(repo, redis_client)
        return repo
