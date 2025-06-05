import asyncio
from sqlalchemy.exc import SQLAlchemyError
from src.db.enums import RoleEnum
from src.schemas.user import UserLogin
from src.db.requests import get_user, create_user
from src.config import settings


async def init_admin():
    role: RoleEnum = RoleEnum.ADMIN
    admin_user = settings.main_admin.get_main_admin()

    try:
        existing_user = await get_user(admin_user.login)
        if existing_user:
            print("[i] Пользователь уже существует")
            return

        new_user = await create_user(admin_user.login, admin_user.password, role)
        print(f"[+] Админ создан: ID = {new_user.id}")

    except SQLAlchemyError as e:
        print(f"[!] Ошибка подключения к БД: {e}")
        exit(1)

    except Exception as e:
        print(f"[!] Непредвиденная ошибка: {e}")
        exit(1)


if __name__ == "__main__":
    asyncio.run(init_admin())
