from fastapi import APIRouter

router = APIRouter(
    prefix="/ejemplo",
    tags=["Ejemplo"]
)

@router.get("/")
def read_root():
    return {"message": "¡Hola desde FastAPI!"}
