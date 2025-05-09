from fastapi import APIRouter

from src.routers.auth import router as auth_router
from src.routers.note import router as note_router
from src.routers.utils import router as utils_router

router = APIRouter()
router.include_router(note_router)
router.include_router(auth_router)
router.include_router(utils_router)
