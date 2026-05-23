from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Response, status

from app.api.deps import CurrentUser, DbSession
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate, UserPasswordChange


router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("/", response_model=List[UserOut])
def list_users(
    db: DbSession,
    current_user: CurrentUser,
    department: Optional[str] = None,
    search: Optional[str] = None,
) -> List[UserOut]:
    query = db.query(User)
    if department:
        query = query.filter(User.department == department)
    if search:
        from sqlalchemy import func, or_
        s = search.lower()
        like = f"%{s}%"
        query = query.filter(
            or_(
                func.lower(User.full_name).like(like),
                func.lower(User.username).like(like),
                func.lower(User.email).like(like),
                func.lower(User.position).like(like),
                User.full_name.contains(search),
                User.position.contains(search),
            )
        )
    users = query.order_by(User.full_name.asc()).all()
    return [UserOut.model_validate(u) for u in users]


@router.get("/departments", response_model=List[str])
def list_departments(db: DbSession, current_user: CurrentUser) -> List[str]:
    rows = db.query(User.department).distinct().all()
    return sorted({r[0] for r in rows if r[0]})


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: DbSession, current_user: CurrentUser) -> UserOut:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return UserOut.model_validate(user)


@router.put("/me", response_model=UserOut)
def update_me(payload: UserUpdate, db: DbSession, current_user: CurrentUser) -> UserOut:
    data = payload.model_dump(exclude_unset=True)
    if "email" in data and data["email"] != current_user.email:
        duplicate = db.query(User).filter(User.email == data["email"], User.id != current_user.id).first()
        if duplicate is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Указанный e-mail уже занят другим сотрудником",
            )
    for field, value in data.items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return UserOut.model_validate(current_user)


@router.post("/me/password", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def change_password(payload: UserPasswordChange, db: DbSession, current_user: CurrentUser):
    if not verify_password(payload.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Текущий пароль введён неверно",
        )
    current_user.password_hash = hash_password(payload.new_password)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
