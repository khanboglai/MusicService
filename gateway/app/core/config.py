from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env", extra='ignore')
    project_name: str = Field("Сервис api gateway", alias="PROJECT_NAME")
    description: str = Field(
        "Маршрутизация запросов пользователей", alias="DESCRIPTION"
    )
    version: str = Field("1.0.0", alias="VERSION")
    cache_host: str = Field("127.0.0.1", alias="CACHE_HOST")
    cache_port: int = Field("6379", alias="CACHE_PORT")
    base_dir: str = str(Path(__file__).parent.parent)


settings = Settings()
