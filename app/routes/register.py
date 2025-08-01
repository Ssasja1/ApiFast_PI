from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from app.db import SessionLocal
from app import models, schemas
from datetime import date

router = APIRouter(prefix="/registro", tags=["Registro"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", status_code=status.HTTP_201_CREATED)
def registrar_usuario(data: schemas.RegistroUsuario, db: Session = Depends(get_db)):
    # Validar email único
    if db.query(models.Usuario).filter_by(email=data.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")

    if data.tipo not in ("atleta", "entrenador"):
        raise HTTPException(status_code=400, detail="Tipo de usuario inválido")

    # Crear usuario
    usuario = models.Usuario(
        email=data.email,
        contrasena_hash=bcrypt.hash(data.contrasena),
        tipo=data.tipo
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    # Crear perfil según tipo
    if data.tipo == "atleta":
        crear_perfil_atleta(usuario.id_usuario, data, db)
    elif data.tipo == "entrenador":
        crear_perfil_entrenador(usuario.id_usuario, data, db)

    return {"mensaje": "Registro exitoso", "id_usuario": usuario.id_usuario, "tipo": usuario.tipo}


def crear_perfil_atleta(user_id: int, data: schemas.RegistroUsuario, db: Session):
    edad = (date.today() - data.fecha_nacimiento).days // 365
    frecuencia_max = 220 - edad

    perfil = models.PerfilAtleta(
        id_usuario=user_id,
        nombre_completo=data.nombre_completo,
        fecha_nacimiento=data.fecha_nacimiento,
        altura=data.altura,
        peso=data.peso,
        deporte=data.deporte,
        frecuencia_cardiaca_minima=data.frecuencia_cardiaca_minima,
        frecuencia_cardiaca_maxima=frecuencia_max,
        id_entrenador=data.id_entrenador if data.id_entrenador else None
    )
    db.add(perfil)
    db.commit()


def crear_perfil_entrenador(user_id: int, data: schemas.RegistroUsuario, db: Session):
    perfil = models.PerfilEntrenador(
        id_usuario=user_id,
        nombre_completo=data.nombre_completo,
        fecha_nacimiento=data.fecha_nacimiento,
        especialidad=data.especialidad,
        experiencia=data.experiencia
    )
    db.add(perfil)
    db.commit()
