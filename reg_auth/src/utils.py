import bcrypt
from datetime import datetime, timedelta
from src.config import settings
import jwt

def get_access_token_lifetime():
    return timedelta(minutes= settings.auth_jwt.access_token_expire)

def get_refresh_token_lifetime():
    return timedelta(hours= settings.auth_jwt.refresh_token_expire)

def create_hash_password(password: str) :
    # print(type(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')))
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def validate_password(password: str, hash_password: str) -> bool:
    return bcrypt.checkpw(password=password.encode('utf-8'), hashed_password=hash_password.encode('utf-8'))

def encode_jwt(payload: dict,  expire_time: timedelta, private_key: str = settings.auth_jwt.private_key_path.read_text(), algorithm: str = settings.auth_jwt.algorithm):
    # int = settings.auth_jwt.access_token_expire_minutes
    to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + expire_time
    to_encode.update(
        exp = expire,
        iat =now,
    )

    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded

def decode_jwt(token: str, public_key: str = settings.auth_jwt.public_key_path.read_text(), algorithm: str = settings.auth_jwt.algorithm) -> dict | None:
    decode = jwt.decode(token, public_key, algorithms=[algorithm])
    return decode