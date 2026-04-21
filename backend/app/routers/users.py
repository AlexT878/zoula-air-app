from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.auth.jwt_bearer import get_current_user, get_current_user_with_roles
from app.models.user import User as UserSchema
from app.db.users import User as UserModel
from app.db.session import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserSchema)
async def read_users_me(
    current_user_id: str = Depends(get_current_user), db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(UserModel.id == current_user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found in database"
        )
    return user


@router.get("/", response_model=List[UserSchema])
async def read_all_users(
    db: Session = Depends(get_db),
    admin_id: str = Depends(get_current_user_with_roles(required_roles=["admin"])),
):
    users = db.query(UserModel).all()
    return users
