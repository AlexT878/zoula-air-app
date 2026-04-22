from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from typing import List
from app.core.errors import ErrorCode
import re


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True


class UserCreate(UserBase):
    full_name: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        if not re.search(r"[a-z]", v):
            raise ValueError(ErrorCode.PASSWORD_NO_LOWER)
        if not re.search(r"[A-Z]", v):
            raise ValueError(ErrorCode.PASSWORD_NO_UPPER)
        if not re.search(r"\d", v):
            raise ValueError(ErrorCode.PASSWORD_NO_DIGIT)
        if not re.search(r"[@$!%*?&]", v):
            raise ValueError(ErrorCode.PASSWORD_NO_SPECIAL)
        return v

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()


class UserInDB(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hashed_password: str
    full_name: str
    roles: List[str] = ["user"]


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    roles: List[str] = ["user"]
