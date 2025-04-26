import os
from enum import Enum

from dotenv import find_dotenv, load_dotenv


class RunMode(Enum):
    DEV = "dev"
    PROD = "prod"
    TEST = "test"


RUN_MODE = RunMode(os.getenv("RUN_MODE", "prod"))
COMPOSE_MODE = os.getenv("COMPOSE_MODE", "false").lower() == "true"

API_PREFIX = os.getenv("API_PREFIX", "/api/v1")

if RUN_MODE == RunMode.DEV:
    dotenv_name = ".env.dev"
    if COMPOSE_MODE:
        dotenv_name = ".env.compose.dev"
elif RUN_MODE == RunMode.TEST:
    dotenv_name = ".env.test"
else:
    dotenv_name = ".env"

load_dotenv(find_dotenv(dotenv_name))


# postgres
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_URL = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# oauth2
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
