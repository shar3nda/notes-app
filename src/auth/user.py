from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlmodel import Session, select

from src.auth.crypto import ALGORITHM, oauth2_scheme, verify_password
from src.db.common import engine
from src.model.token import TokenData
from src.model.user import User
from src.settings import SECRET_KEY


def get_user(username: str) -> User | None:
    with Session(engine) as session:
        stmt = select(User).where(User.username == username)
        return session.exec(stmt).first()


def authenticate_user(username: str, password: str) -> User | None:
    user = get_user(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user
