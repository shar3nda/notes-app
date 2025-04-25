from fastapi import FastAPI

from routers.main import router as api_router
from settings import API_PREFIX

app = FastAPI(root_path=API_PREFIX)

app.include_router(api_router)
