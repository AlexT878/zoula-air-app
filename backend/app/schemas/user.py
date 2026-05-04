from datetime import date

from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from typing import List
from app.constants.enums import Gender
from app.core.errors import ErrorCode
import re
from app.schemas.token import Token


class UserMinimal(BaseModel):
    id: int
    first_name: str
    roles: List[str]


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserMinimal


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    birth_date: date
    gender: Gender
    country: str = Field(..., min_length=2, max_length=60)
    phone_country_code: str = Field(..., pattern=r"^\+\d{1,4}$")
    phone_number: str = Field(..., pattern=r"^\d{7,15}$")


class UserCreate(UserBase):
    email: EmailStr = Field(..., min_length=3, max_length=254)
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=8, max_length=64)
    birth_date: date
    gender: Gender
    country: str = Field(..., min_length=2, max_length=60)
    phone_country_code: str = Field(..., pattern=r"^\+\d{1,4}$")
    phone_number: str = Field(..., pattern=r"^\d{7,15}$")

    @field_validator("birth_date")
    @classmethod
    def validate_age(cls, v: date) -> date:
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 13:
            raise ValueError("You must be at least 13 years old.")
        if age > 150:
            raise ValueError("Invalid date of birth.")
        return v

    @field_validator("first_name", "last_name")
    @classmethod
    def name_must_not_contain_numbers(cls, v: str) -> str:
        if any(char.isdigit() for char in v):
            raise ValueError("The name cannot contain numbers.")
        return v.strip().title()

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
    first_name: str
    roles: List[str] = ["user"]


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    roles: List[str] = ["user"]
