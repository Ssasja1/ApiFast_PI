from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Usuario
from passlib.context import CryptContext

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginInput(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(data: LoginInput, db: Session = Depends(get_db)):  # <-- Aquí está el cambio importante
    usuario = db.query(Usuario).filter(Usuario.email == data.email).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Correo no encontrado")

    if not pwd_context.verify(data.password, usuario.contrasena_hash):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return {
        "mensaje": "Login exitoso",
        "usuario": {
            "id_usuario": usuario.id_usuario,
            "email": usuario.email,
            "tipo": usuario.tipo
        }
    }
