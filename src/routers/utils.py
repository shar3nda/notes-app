from fastapi import APIRouter

router = APIRouter(
    prefix="/utils",
    tags=["utils"],
    responses={404: {"description": "Not found"}},
)


@router.get("/ping")
def ping():
    return "pong"
