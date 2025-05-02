import enum
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from db.database import Base

class RoleEnum(str, enum.Enum):
    LISTNER = "слушатель"
    AUTHOR = "автор"
    ADMIN = "админ"

class User(Base):

    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[RoleEnum] = mapped_column(
        default=RoleEnum.LISTNER,
        server_default=text("'слушатель'")
    )

    