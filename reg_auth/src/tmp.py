import bcrypt
from datetime import datetime, timedelta
from config import settings
import jwt

from pathlib import Path

BASE_DIR = Path(__file__).parent

Path = BASE_DIR / "certs"

print(Path)

public_key: str = settings.auth_jwt.public_key_path.read_text()

print(public_key)
