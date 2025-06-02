from datetime import datetime
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from src.api.v1.artists import router
from src.dependencies.repository import get_artist_repository
from src.models.artist import Artist
from src.repositories.domain_repo import ArtistRepositoryABC
from src.value_objects.artist_description import Description

app = FastAPI()
app.include_router(router)
client = TestClient(app)


# @pytest.mark.asyncio
# async def test_get_artist():
#     mock_repo = AsyncMock(spec=ArtistRepositoryABC)
#     mock_repo.get_artist_by_user_id.return_value = Artist(
#         name="Test Artist",
#         email="fakemail@gmail.com",
#         registered_at=datetime.now(),
#         description=Description("Test Artist"),
#         user_id=1
#     )
#
#     app.dependency_overrides[get_artist_repository] = lambda: mock_repo
#
#     response = client.get("/1")
#     assert response.status_code == 200
#     assert response.json() == {"message": "Test Artist"}
#
#     mock_repo.get_artist_by_user_id.assert_called_once_with(1)
#     app.dependency_overrides.clear()
#

@pytest.mark.asyncio
async def test_create_artist():
    # создаем мок репозитория
    mock_repo = AsyncMock(spec=ArtistRepositoryABC)
    mock_repo.create_artist.return_value = Artist(
        name="Test Artist",
        email="fakemail@gmail.com",
        registered_at="2023-01-01",
        description=Description("Test description"),
        user_id=1
    )

    # переопределяем зависимость
    app.dependency_overrides[get_artist_repository] = lambda: mock_repo

    artist_data = {
        "name": "Test Artist",
        "email": "fakemail@gmail.com",
        "registered_at": "2023-01-01",
        "description": "Test description",
        "user_id": 1
    }

    response = client.post("/create", json=artist_data)

    assert response.status_code == 200
    expected_response = {"message": "Test Artist"}
    assert response.json() == expected_response

    mock_repo.create_artist.assert_called_once()
    # восстанавливаем исходные зависимости
    app.dependency_overrides.clear()