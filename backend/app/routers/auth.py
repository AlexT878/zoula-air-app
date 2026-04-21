from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from pydantic import ValidationError

from app.auth.jwt_handler import create_access_token, create_refresh_token, decode_token
from app.auth.utils import verify_password, get_password_hash
from app.core.config import settings
from app.models.token import Token
from app.models.user import UserCreate, User as UserSchema
from app.db.users import User as UserModel
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED
)
async def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user_exists = db.query(UserModel).filter(UserModel.email == user_in.email).first()
    if user_exists:
        raise HTTPException(
            status_code=400, detail="A user with this email already exists."
        )

    hashed_password = get_password_hash(user_in.password)

    new_user = UserModel(
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
        is_active=True,
        roles=["user"],
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
async def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id),
        roles=user.roles,
        expires_delta=access_token_expires,
    )
    refresh_token = create_refresh_token(subject=str(user.id))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    refresh_token: str = Body(..., embed=True), db: Session = Depends(get_db)
) -> Any:
    try:
        payload = decode_token(refresh_token)
        if payload.get("token_type") != "refresh":
            raise HTTPException(status_code=403, detail="Invalid token type")

        user_id = payload.get("sub")
        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="User not found or inactive")

        access_token = create_access_token(subject=str(user.id), roles=user.roles)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
    except (JWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credentials")
