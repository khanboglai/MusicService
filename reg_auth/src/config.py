import os
import yaml
import logging
import logging.config
from pathlib import Path
from pydantic import BaseModel
from src.schemas.user import UserLogin
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent

config_path: Path = BASE_DIR / "logger" / "log_conf.yaml"

with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f.read())

logging.config.dictConfig(config)
logger = logging.getLogger(__name__)


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"
    access_token_expire: int = 60 #minutes
    refresh_token_expire: int = 3 #hours

class MainAdmin(BaseModel):
    MAIN_ADMIN_NAME: str
    MAIN_ADMIN_PASS: str

    def get_main_admin(self) -> UserLogin:
        return UserLogin(
            login=self.MAIN_ADMIN_NAME,
            password=self.MAIN_ADMIN_PASS
        )

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    
    MAIN_ADMIN_NAME: str
    MAIN_ADMIN_PASS: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

    def get_db_url(self):
        return (f"postgresql+asyncpg://server:password@"
                f"auth_service_postgre:5432/auth_service_db")
    
    auth_jwt: AuthJWT = AuthJWT()


    @property
    def main_admin(self) -> MainAdmin:
        return MainAdmin(
            MAIN_ADMIN_NAME=self.MAIN_ADMIN_NAME,
            MAIN_ADMIN_PASS=self.MAIN_ADMIN_PASS
        )



settings = Settings()