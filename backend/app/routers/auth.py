from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from pydantic import ValidationError

from app.auth.jwt_handler import create_access_token, create_refresh_token, decode_token
from app.auth.utils import verify_password, get_password_hash
from app.core.config import settings
from app.schemas.token import Token
from app.schemas.user import UserCreate, User as UserSchema
from app.models.users import User as UserModel
from app.db.session import get_db

from app.core.errors import ErrorCode

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED
)
async def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    user_exists = db.query(UserModel).filter(UserModel.email == user_in.email).first()
    if user_exists:
        raise HTTPException(
            status_code=400,
            detail={
                "code": ErrorCode.EMAIL_ALREADY_EXISTS,
                "message": ErrorCode.EMAIL_ALREADY_EXISTS_MESSAGE,
            },
        )

    hashed_password = get_password_hash(user_in.password)

    new_user = UserModel(
        email=user_in.email,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        birth_date=user_in.birth_date,
        gender=user_in.gender,
        country=user_in.country,
        phone_country_code=user_in.phone_country_code,
        phone_number=user_in.phone_number,
        hashed_password=hashed_password,
        is_active=True,
        roles=["user"],
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
async def login_for_access_token(
    response: Response,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorCode.INCORRECT_LOGIN,
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(status_code=400, detail=ErrorCode.INACTIVE_USER)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=str(user.id),
        roles=user.roles,
        expires_delta=access_token_expires,
    )
    refresh_token = create_refresh_token(subject=str(user.id))

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,  # 86400 = 1 day in seconds
        path="/",
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    refresh_token: str | None = Cookie(None),
    db: Session = Depends(get_db),
) -> Any:
    if not refresh_token:
        raise HTTPException(
            status_code=401, detail="Refresh token missing from cookies"
        )

    try:
        payload = decode_token(refresh_token)
        if payload.get("token_type") != "refresh":
            raise HTTPException(status_code=403, detail=ErrorCode.TOKEN_INVALID_TYPE)

        user_id = payload.get("sub")
        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user or not user.is_active:
            raise HTTPException(
                status_code=401, detail=ErrorCode.USER_NOT_FOUND_INACTIVE_MESSAGE
            )

        access_token = create_access_token(subject=str(user.id), roles=user.roles)

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
    except (JWTError, ValidationError):
        raise HTTPException(status_code=403, detail=ErrorCode.TOKEN_INVALID_CREDENTIALS)
