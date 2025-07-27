from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models, schemas
from passlib.hash import bcrypt
from datetime import datetime
from typing import List

router = APIRouter(prefix="/entrenadores", tags=["Entrenadores"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST - Crear entrenador
@router.post("/", response_model=schemas.EntrenadorResponse, status_code=status.HTTP_201_CREATED)
def crear_entrenador(data: schemas.EntrenadorCreate, db: Session = Depends(get_db)):
    # Validar que el correo no exista
    if db.query(models.Usuario).filter_by(email=data.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")

    # Crear usuario
    usuario = models.Usuario(
        email=data.email,
        contrasena_hash=bcrypt.hash(data.contrasena),
        tipo="entrenador"
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    # Crear perfil de entrenador
    perfil = models.PerfilEntrenador(
        id_usuario=usuario.id_usuario,
        nombre_completo=data.nombre_completo,
        fecha_nacimiento=data.fecha_nacimiento,
        especialidad=data.especialidad,
        experiencia=data.experiencia
    )
    db.add(perfil)
    db.commit()
    db.refresh(perfil)

    return {
        "id_entrenador": perfil.id_entrenador,
        "id_usuario": usuario.id_usuario,
        "email": usuario.email,
        "tipo": usuario.tipo,
        "nombre_completo": perfil.nombre_completo,
        "fecha_nacimiento": perfil.fecha_nacimiento,
        "especialidad": perfil.especialidad,
        "experiencia": perfil.experiencia,
        "fecha_registro": usuario.fecha_registro,
        "activo": usuario.activo
    }

# GET - Listar todos los entrenadores
@router.get("/", response_model=List[schemas.EntrenadorResponse])
def listar_entrenadores(db: Session = Depends(get_db)):
    resultados = db.query(
        models.PerfilEntrenador,
        models.Usuario
    ).join(
        models.Usuario,
        models.PerfilEntrenador.id_usuario == models.Usuario.id_usuario
    ).filter(
        models.Usuario.tipo == "entrenador"
    ).all()

    entrenadores = []
    for perfil, usuario in resultados:
        entrenadores.append({
            "id_entrenador": perfil.id_entrenador,
            "id_usuario": usuario.id_usuario,
            "email": usuario.email,
            "tipo": usuario.tipo,
            "nombre_completo": perfil.nombre_completo,
            "fecha_nacimiento": perfil.fecha_nacimiento,
            "especialidad": perfil.especialidad,
            "experiencia": perfil.experiencia,
            "fecha_registro": usuario.fecha_registro,
            "activo": usuario.activo
        })
    
    return entrenadores

# GET - Obtener un entrenador por ID
@router.get("/{entrenador_id}", response_model=schemas.EntrenadorResponse)
def obtener_entrenador(entrenador_id: int, db: Session = Depends(get_db)):
    resultado = db.query(
        models.PerfilEntrenador,
        models.Usuario
    ).join(
        models.Usuario,
        models.PerfilEntrenador.id_usuario == models.Usuario.id_usuario
    ).filter(
        models.PerfilEntrenador.id_entrenador == entrenador_id,
        models.Usuario.tipo == "entrenador"
    ).first()

    if not resultado:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    
    perfil, usuario = resultado

    return {
        "id_entrenador": perfil.id_entrenador,
        "id_usuario": usuario.id_usuario,
        "email": usuario.email,
        "tipo": usuario.tipo,
        "nombre_completo": perfil.nombre_completo,
        "fecha_nacimiento": perfil.fecha_nacimiento,
        "especialidad": perfil.especialidad,
        "experiencia": perfil.experiencia,
        "fecha_registro": usuario.fecha_registro,
        "activo": usuario.activo
    }

# PUT - Actualizar un entrenador
@router.put("/{entrenador_id}", response_model=schemas.EntrenadorResponse)
def actualizar_entrenador(
    entrenador_id: int, 
    data: schemas.EntrenadorUpdate,
    db: Session = Depends(get_db)
):
    resultado = db.query(
        models.PerfilEntrenador,
        models.Usuario
    ).join(
        models.Usuario,
        models.PerfilEntrenador.id_usuario == models.Usuario.id_usuario
    ).filter(
        models.PerfilEntrenador.id_entrenador == entrenador_id,
        models.Usuario.tipo == "entrenador"
    ).first()

    if not resultado:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    
    perfil, usuario = resultado

    # Actualizar campos
    if data.nombre_completo:
        perfil.nombre_completo = data.nombre_completo
    if data.fecha_nacimiento:
        perfil.fecha_nacimiento = data.fecha_nacimiento
    if data.especialidad:
        perfil.especialidad = data.especialidad
    if data.experiencia:
        perfil.experiencia = data.experiencia
    
    db.commit()
    db.refresh(perfil)

    return {
        "id_entrenador": perfil.id_entrenador,
        "id_usuario": usuario.id_usuario,
        "email": usuario.email,
        "tipo": usuario.tipo,
        "nombre_completo": perfil.nombre_completo,
        "fecha_nacimiento": perfil.fecha_nacimiento,
        "especialidad": perfil.especialidad,
        "experiencia": perfil.experiencia,
        "fecha_registro": usuario.fecha_registro,
        "activo": usuario.activo
    }

# DELETE - Eliminar un entrenador
@router.delete("/{entrenador_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_entrenador(entrenador_id: int, db: Session = Depends(get_db)):
    resultado = db.query(
        models.PerfilEntrenador,
        models.Usuario
    ).join(
        models.Usuario,
        models.PerfilEntrenador.id_usuario == models.Usuario.id_usuario
    ).filter(
        models.PerfilEntrenador.id_entrenador == entrenador_id,
        models.Usuario.tipo == "entrenador"
    ).first()

    if not resultado:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    
    perfil, usuario = resultado

    # Eliminar en orden correcto
    db.delete(perfil)
    db.delete(usuario)
    db.commit()
    
    return None