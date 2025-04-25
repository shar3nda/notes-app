from fastapi import APIRouter

from src.routers.note import router as note_router

router = APIRouter()
router.include_router(note_router)
