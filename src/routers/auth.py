from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, status
from sqlmodel import Session

from src.auth.crypto import (
    create_access_token,
    create_refresh_token,
    get_new_access_token,
    hash_password,
)
from src.auth.user import authenticate_user, get_user
from src.db.common import engine
from src.model.token import Token
from src.model.user import AuthForm, User, UserCreate

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register")
def register(user: UserCreate) -> Token:
    if get_user(user.username):
        raise HTTPException(status_code=400, detail="Username taken")
    hashed = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed)
    with Session(engine) as session:
        session.add(new_user)
        session.commit()
    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[AuthForm, Form()],
) -> Token:
    if form_data.grant_type == "refresh_token":
        new_access_token = get_new_access_token(form_data.refresh_token)

        return Token(
            access_token=new_access_token,
            refresh_token=form_data.refresh_token,
        )

    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return Token(access_token=access_token, refresh_token=refresh_token)
