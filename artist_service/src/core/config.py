from pathlib import Path

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env")
    project_name: str = Field("Сервис для работы с данными исполнителя", alias="PROJECT_NAME")
    description: str = Field(
        "Обработка данных исполнителя и отображение прослушиваний", alias="DESCRIPTION"
    )
    version: str = Field("1.0.0", alias="VERSION")
    cache_host: str = Field("127.0.0.1", alias="CACHE_HOST")
    cache_port: int = Field("6379", alias="CACHE_PORT")
    base_dir: str = str(Path(__file__).parent.parent)
    postgres_dsn: PostgresDsn = Field(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/todos",
        alias="POSTGRES_DSN",
    )
    echo: bool = Field(True, alias="ECHO")


settings = Settings()
