from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI

from src.routers.main import router as api_router
from src.settings import API_PREFIX

app = FastAPI(root_path=API_PREFIX)
app.add_middleware(CorrelationIdMiddleware)

app.include_router(api_router)
