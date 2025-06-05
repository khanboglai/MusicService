from pathlib import Path
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """ Класс настроек приложения """
    model_config = SettingsConfigDict(env_prefix="", env_file=".env", extra="ignore")
    project_name: str = Field("Сервис для чтения метаданных", alias="PROJECT_NAME")
    description: str = Field(
        "Чтение метаданных контента (треков и альбомов) в базу данных", alias="DESCRIPTION"
    )
    version: str = Field("1.0.0", alias="VERSION")
    base_dir: str = str(Path(__file__).parent.parent)

    # Переменные для подключения к базе данных
    postgres_user: str = Field(..., alias="DB_USER")
    postgres_password: str = Field(..., alias="DB_PASSWORD")
    postgres_db: str = Field(..., alias="DB_NAME")

    echo: bool = Field(True, alias="ECHO")

    @property
    def postgres_dsn(self) -> PostgresDsn:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@metadata_database:5432/{self.postgres_db}"


settings = Settings()
