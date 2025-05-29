import os
from pathlib import Path
from pydantic import BaseModel
from src.schemas.user import UserLogin
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"
    access_token_expire: int = 15 #minutes
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
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
    
    auth_jwt: AuthJWT = AuthJWT()


    @property
    def main_admin(self) -> MainAdmin:
        return MainAdmin(
            MAIN_ADMIN_NAME=self.MAIN_ADMIN_NAME,
            MAIN_ADMIN_PASS=self.MAIN_ADMIN_PASS
        )



settings = Settings()