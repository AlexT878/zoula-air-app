from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True


class UserCreate(UserBase):
    password: str
    full_name: str


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
