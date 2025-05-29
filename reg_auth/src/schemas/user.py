from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date

class UserLogin(BaseModel):
    login: EmailStr = Field(default=..., description="Email")
    password: str = Field(default=..., min_length=6, max_length=50, description="Password length must be more than 5 and less then 51")
    # role: RoleEnum = RoleEnum.LISTNER

    @field_validator('login')
    def normalize_email(cls, v: str) -> str:
        return v.lower()