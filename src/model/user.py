from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, min_length=3, max_length=50)
    hashed_password: str


class UserCreate(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    username: str


class AuthForm(BaseModel):
    username: str | None = None
    password: str | None = None
    grant_type: str | None = None
    refresh_token: str | None = None
