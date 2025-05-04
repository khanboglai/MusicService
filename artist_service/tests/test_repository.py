from datetime import datetime
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from sqlalchemy.exc import IntegrityError
from src.repositories.artist_repo import ArtistRepository
from src.models.artist import Artist
from src.value_objects.artist_description import Description
from src.domain_exceptions import *


@pytest.mark.asyncio
async def test_create_artist():
    mock_db = AsyncMock()
    mock_db.add = MagicMock()
    repo = ArtistRepository(db=mock_db)

    new_artist = Artist(
        name="Test Artist",
        email="fakemail@gmail.com",
        registered_at=datetime.now(),
        cover_path="Test.png",
        description=Description("Test Artist")
    )

    created_artist = await repo.create_artist(new_artist)
    mock_db.add.assert_called_once_with(new_artist)
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(new_artist)

    assert created_artist == new_artist


@pytest.mark.asyncio
async def test_create_existing_artist():
    mock_db = AsyncMock()
    mock_db.add = MagicMock()
    repo = ArtistRepository(db=mock_db)

    new_artist = Artist(
        name="Test Artist",
        email="fakemail@gmail.com",
        registered_at=datetime.now(),
        cover_path="Test.png",
        description=Description("Test Artist")
    )

    # моделируем ошибку уникальности с нужной строкой в сообщении
    mock_db.commit.side_effect = IntegrityError(
        'duplicate key value violates unique constraint "artists_name_key"\nDETAIL: Key (name)=(Test Artist) already exists.',
        orig=None,
        params=None
    )

    with pytest.raises(UniqueViolationException) as exc_info:
        await repo.create_artist(new_artist)

    assert "Исполнитель Test Artist уже существует" in str(exc_info.value)

    # проверяем, что методы базы данных вызывались корректно
    mock_db.add.assert_called_once_with(new_artist)
    mock_db.commit.assert_called_once()
    mock_db.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_delete_artist():
    mock_db = AsyncMock()
    repo = ArtistRepository(db=mock_db)

    artist = Artist(
        name="Test Artist",
        email="test@example.com",
        registered_at=None,
        cover_path="test.png",
        description=Description("Test description")
    )
    artist.oid = 1

    repo.get_artist_by_id = AsyncMock(return_value=artist)

    result = await repo.delete_artist(artist.oid)
    assert result == artist.name

    repo.get_artist_by_id.assert_called_once_with(artist.oid)
    mock_db.delete.assert_called_once_with(artist)
    mock_db.commit.assert_called_once()


# @pytest.mark.asyncio
# async def test_delete_artist_not_exist():
#     # Создаём мок для базы данных
#     mock_db = AsyncMock()
#
#     # Создаём экземпляр репозитория
#     repo = ArtistRepository(db=mock_db)
#
#     # Мокируем метод get_artist_by_oid
#     repo.get_artist_by_oid = AsyncMock(return_value=None)
#
#     # Проверяем, что выбрасывается исключение NotFoundException
#     with pytest.raises(InvalidIdException) as exc_info:
#         await repo.delete_artist(999)
#
#     # Проверяем сообщение исключения
#     assert "Исполнитель с id: 999 не существует" in str(exc_info.value)
#
#     # Проверяем вызовы методов базы данных
#     repo.get_artist_by_oid.assert_called_once_with(999)
#     mock_db.delete.assert_not_called()
#     mock_db.commit.assert_not_called()