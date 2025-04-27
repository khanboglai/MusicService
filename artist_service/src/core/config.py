from pathlib import Path
import os
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env", extra='ignore')
    project_name: str = Field("Сервис для работы с данными исполнителя", alias="PROJECT_NAME")
    description: str = Field(
        "Обработка данных исполнителя и отображение прослушиваний", alias="DESCRIPTION"
    )
    version: str = Field("1.0.0", alias="VERSION")
    cache_host: str = Field("127.0.0.1", alias="CACHE_HOST")
    cache_port: int = Field("6379", alias="CACHE_PORT")
    base_dir: str = str(Path(__file__).parent.parent)

    # Переменные для подключения к базе данных
    postgres_user: str = Field(..., alias="DB_USER")
    postgres_password: str = Field(..., alias="DB_PASSWORD")
    postgres_db: str = Field(..., alias="DB_NAME")

    echo: bool = Field(True, alias="ECHO")

    @property
    def postgres_dsn(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@artist_service_db:5432/{self.postgres_db}"


settings = Settings()
