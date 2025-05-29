from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from src.db.database import Base
from src.db.enums import RoleEnum

class User(Base):

    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[RoleEnum] = mapped_column(
        default=RoleEnum.LISTNER,
    )

    