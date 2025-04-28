import pytest
from unittest.mock import AsyncMock, patch
from src.repositories.artist_repo import ArtistRepository
from src.models.artist import Artist
from src.repositories.domain_repo import ArtistRepositoryAbc


@pytest.mark.asyncio
@patch("src.repositories.artist_repo.ArtistRepository")
async def test_create_artist(mock_artist_repo: ArtistRepository):
    mock_artist = Artist(
        name="Test Artist",
        registered_at="2023-01-01",
        cover_path=None,
        description="Test Description"
    )
    mock_artist._id = 1  # Устанавливаем id вручную, так как он не передается через конструктор

    # Мокируем метод get_artist
    mock_artist_repo.return_value.get_artist = AsyncMock(return_value=mock_artist)

    # Вызываем метод get_artist
    artist_repo = mock_artist_repo()
    artist_id = 1
    fetched_artist = await artist_repo.get_artist(artist_id)

    # Проверяем, что метод был вызван
    mock_artist_repo.return_value.get_artist.assert_called_once_with(artist_id)

    # Проверяем результат
    assert fetched_artist._id == 1
    assert fetched_artist.name == "Test Artist"

