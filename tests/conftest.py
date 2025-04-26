import os

import psycopg
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, delete

from src.auth.crypto import hash_password
from src.main import app
from src.model.user import User
from src.settings import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_URL,
    POSTGRES_USER,
)


def create_database_if_not_exists():
    conn = psycopg.connect(
        dbname="postgres",
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
    )
    conn.autocommit = True

    with conn.cursor() as cursor:
        cursor.execute(f"DROP DATABASE IF EXISTS {POSTGRES_DB}")
        cursor.execute(f"CREATE DATABASE {POSTGRES_DB}")

    conn.close()


TEST_USER = {
    "username": "testuser",
    "password": "StrongPassword123!",
}


def cleanup_users():
    engine = create_engine(POSTGRES_URL)
    with Session(engine) as session:
        session.exec(delete(User))
        session.commit()


@pytest.fixture
def test_user_data():
    yield TEST_USER
    cleanup_users()


@pytest.fixture
def test_user():
    engine = create_engine(POSTGRES_URL)
    hashed = hash_password(TEST_USER["password"])
    new_user = User(username=TEST_USER["username"], hashed_password=hashed)
    with Session(engine) as session:
        session.add(new_user)
        session.commit()
    yield TEST_USER
    cleanup_users()


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    os.environ["RUN_MODE"] = "test"
    create_database_if_not_exists()

    engine = create_engine(POSTGRES_URL)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    yield


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
