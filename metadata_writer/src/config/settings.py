from pathlib import Path

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings

class ServiceSettings(BaseSettings):
    project_name: str = Field(
        "",
        alias="PROJECT_NAME"
    )
    description: str = Field(
        "",
        alias="DESCRIPTION"
    )
    base_dir : str = str(Path(__file__).parent.parent)
    postgres_dsn: PostgresDsn = Field()

settings = ServiceSettings()