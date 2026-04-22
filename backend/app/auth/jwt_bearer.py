from datetime import datetime, timezone
from typing import List, Optional, Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError

from app.auth.jwt_handler import decode_token
from app.core.config import settings
from app.schemas.token import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = decode_token(token)
        token_data = TokenPayload(**payload)

        if token_data.sub is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is missing subject (user ID)",
            )
        return token_data.sub

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_with_roles(required_roles: List[str]) -> Callable:
    async def _role_checker(token: str = Depends(oauth2_scheme)) -> str:
        try:
            payload = decode_token(token)
            token_data = TokenPayload(**payload)

            if not token_data.sub:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            user_roles = token_data.roles

            if "admin" in user_roles:
                return token_data.sub

            if not any(role in user_roles for role in required_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Missing required roles: {required_roles}",
                )

            return token_data.sub

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
            )
        except (JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
            )

    return _role_checker
