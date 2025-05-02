from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
import bcrypt
from db.database import async_session_maker as session_fabric
from db.models import User, RoleEnum
from utils import create_hash_password

async def get_user(new_login: str) -> User | None:
    try:
        async with session_fabric() as session:
            result = await session.execute(select(User).where(User.login == new_login))
            return result.scalar_one_or_none()
            
    except SQLAlchemyError as e:
        raise e


async def create_user(new_login: str, password: str, role: RoleEnum) -> User | None:
    try:
        async with session_fabric() as session:
            hashed_password = create_hash_password(password)

            new_user = User(login=new_login, password=hashed_password, role=role)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)  
            return new_user

    except SQLAlchemyError as e:
        raise e

async def get_password(login: str) -> str | None:
    try:
        async with session_fabric() as session:
            result = await session.execute(select(User.password).where(User.login == login))
            return result.scalar_one_or_none()
            
    except SQLAlchemyError as e:
        raise e



# async def check_password():


# async def change_role():
