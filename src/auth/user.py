from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt
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


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    expired_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except ExpiredSignatureError:
        raise expired_exception
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


def is_allowed_username(u: str) -> str:
    if len(u) < 3:
        raise ValueError("Username must be at least 3 characters long")
    if len(u) > 50:
        raise ValueError("Username must be no more than 50 characters long")
    if not u.isalnum():
        raise ValueError("Username must contain only numbers and digits")
    return u


def is_strong_password(p: str) -> str:
    if len(p) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if len(p) > 50:
        raise ValueError("Password must be no more than 50 characters long")
    if not any(c.isdigit() for c in p):
        raise ValueError("Password must contain at least one number")
    if not any(c.islower() for c in p):
        raise ValueError("Password must contain at least one lowercase letter")
    if not any(c.isupper() for c in p):
        raise ValueError("Password must contain at least one uppercase letter")
    return p
