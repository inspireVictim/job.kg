from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


RoleType = Literal["employee", "hr", "admin"]


class UserBase(BaseModel):
    username: str = Field(min_length=2, max_length=64, pattern=r"^[A-Za-z0-9_.-]+$")
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=128)
    department: str = Field(default="Общий отдел", max_length=64)
    position: str = Field(default="Сотрудник", max_length=64)
    phone: Optional[str] = Field(default=None, max_length=32)
    role: RoleType = "employee"


class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=128)


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(default=None, min_length=2, max_length=128)
    department: Optional[str] = Field(default=None, max_length=64)
    position: Optional[str] = Field(default=None, max_length=64)
    phone: Optional[str] = Field(default=None, max_length=32)
    email: Optional[EmailStr] = None


class UserPasswordChange(BaseModel):
    old_password: str = Field(min_length=6)
    new_password: str = Field(min_length=6, max_length=128)


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
