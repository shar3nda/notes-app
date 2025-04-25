from typing import Literal

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    username: str


class AuthForm(BaseModel):
    username: str | None = None
    password: str | None = None
    grant_type: Literal["password", "refresh_token"] = "password"
    refresh_token: str | None = None
