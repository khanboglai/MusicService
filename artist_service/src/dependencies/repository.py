""" Тут зависимости для слоя репозитория """
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.postgres import get_session
from src.repositories.artist_repo import ArtistRepository
from src.repositories.domain_repo import ArtistRepositoryABC


def get_artist_repository(db: AsyncSession = Depends(get_session)) -> ArtistRepositoryABC:
    """
    Функция для возврата нужного репозитория
    Здесь надо будет прописать репозиторий, который работает с кешированием
    """
    return ArtistRepository(db)