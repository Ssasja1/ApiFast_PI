from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models, schemas
from passlib.hash import bcrypt
from datetime import date
from typing import List

router = APIRouter(prefix="/atletas", tags=["Atletas"])

# Dependencia para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.AtletaResponse)
def crear_atleta(data: schemas.AtletaCreate, db: Session = Depends(get_db)):
    # Validar que el correo no exista
    if db.query(models.Usuario).filter_by(email=data.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")

    edad = (date.today() - data.fecha_nacimiento).days // 365
    frecuencia_max = 220 - edad

    # Crear usuario
    usuario = models.Usuario(
        email=data.email,
        contrasena_hash=bcrypt.hash(data.contrasena),
        tipo="atleta"
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    # Crear perfil de atleta
    perfil = models.PerfilAtleta(
        id_usuario=usuario.id_usuario,
        nombre_completo=data.nombre_completo,
        fecha_nacimiento=data.fecha_nacimiento,
        altura=data.altura,
        peso=data.peso,
        deporte=data.deporte,
        id_entrenador=data.id_entrenador if data.id_entrenador else None,
        frecuencia_cardiaca_minima=data.frecuencia_cardiaca_minima,
        frecuencia_cardiaca_maxima=frecuencia_max
    )
    db.add(perfil)
    db.commit()

    return {
    "id_usuario": usuario.id_usuario,
    "email": usuario.email,
    "tipo": usuario.tipo,
    "nombre_completo": perfil.nombre_completo,
    "fecha_nacimiento": perfil.fecha_nacimiento,
    "altura": perfil.altura,
    "peso": perfil.peso,
    "deporte": perfil.deporte,
    "id_entrenador": perfil.id_entrenador,
    "frecuencia_cardiaca_minima": perfil.frecuencia_cardiaca_minima,
    "frecuencia_cardiaca_maxima": perfil.frecuencia_cardiaca_maxima,
    "id_atleta": perfil.id_atleta 
    }


#GET (Listar todos los atletas)
@router.get("/", response_model=List[schemas.AtletaResponse])
def listar_atletas(db: Session = Depends(get_db)):
    """Lista todos los atletas registrados con sus perfiles"""
    atletas = db.query(models.Usuario).filter_by(tipo="atleta").all()
    
    result = []
    for usuario in atletas:
        perfil = db.query(models.PerfilAtleta).filter_by(id_usuario=usuario.id_usuario).first()
        if perfil:
            result.append({
        "id_atleta": perfil.id_atleta,         
        "id_usuario": usuario.id_usuario,
        "email": usuario.email,
        "tipo": usuario.tipo,
        "nombre_completo": perfil.nombre_completo,
        "fecha_nacimiento": perfil.fecha_nacimiento,
        "altura": perfil.altura,
        "peso": perfil.peso,
        "deporte": perfil.deporte,
        "id_entrenador": perfil.id_entrenador,
        "frecuencia_cardiaca_minima": perfil.frecuencia_cardiaca_minima,
        "frecuencia_cardiaca_maxima": perfil.frecuencia_cardiaca_maxima
            })
    
    return result

#GET (Obtener un atleta por ID)
@router.get("/{atleta_id}", response_model=schemas.AtletaResponse)
def obtener_atleta(atleta_id: int, db: Session = Depends(get_db)):
    """Obtiene un atleta por ID de perfil (id_atleta)"""
    perfil = db.query(models.PerfilAtleta).filter_by(id_atleta=atleta_id).first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil de atleta no encontrado")
    
    usuario = db.query(models.Usuario).filter_by(id_usuario=perfil.id_usuario).first()
    if not usuario or usuario.tipo != "atleta":
        raise HTTPException(status_code=404, detail="Usuario atleta no encontrado")
    
    return {
        "id_atleta": perfil.id_atleta,  # Nuevo campo
        "id_usuario": usuario.id_usuario,
        "email": usuario.email,
        "tipo": usuario.tipo,
        "fecha_registro": usuario.fecha_registro,  # Nuevo campo
        "activo": usuario.activo,  # Nuevo campo
        "nombre_completo": perfil.nombre_completo,
        "fecha_nacimiento": perfil.fecha_nacimiento,  # Nuevo campo
        "altura": perfil.altura,  # Nuevo campo
        "peso": perfil.peso,  # Nuevo campo
        "deporte": perfil.deporte,
        "id_entrenador": perfil.id_entrenador,  # Nuevo campo
        "frecuencia_cardiaca_minima": perfil.frecuencia_cardiaca_minima,  # Nuevo campo
        "frecuencia_cardiaca_maxima": perfil.frecuencia_cardiaca_maxima  # Nuevo campo
    }


#PUT (Actualizar un atleta)
@router.put("/{atleta_id}", response_model=schemas.AtletaResponse)
def actualizar_atleta(
    atleta_id: int, 
    data: schemas.AtletaUpdate,
    db: Session = Depends(get_db)
):
    """Actualiza la información de un atleta por ID de perfil (id_atleta)"""
    # Primero buscar el perfil del atleta
    perfil = db.query(models.PerfilAtleta).filter_by(id_atleta=atleta_id).first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil de atleta no encontrado")
    
    # Luego buscar el usuario asociado
    usuario = db.query(models.Usuario).filter_by(id_usuario=perfil.id_usuario, tipo="atleta").first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario atleta no encontrado")

    # Actualizar campos permitidos
    if data.nombre_completo:
        perfil.nombre_completo = data.nombre_completo
    if data.altura:
        perfil.altura = data.altura
    if data.peso:
        perfil.peso = data.peso
    if data.deporte:
        perfil.deporte = data.deporte
    if data.id_entrenador is not None:
        perfil.id_entrenador = data.id_entrenador
    if data.frecuencia_cardiaca_minima:
        perfil.frecuencia_cardiaca_minima = data.frecuencia_cardiaca_minima
    
    db.commit()
    db.refresh(perfil)

    return {
        "id_atleta": perfil.id_atleta,
        "id_usuario": usuario.id_usuario,
        "email": usuario.email,
        "tipo": usuario.tipo,
        "nombre_completo": perfil.nombre_completo,
        "fecha_nacimiento": perfil.fecha_nacimiento,
        "altura": perfil.altura,
        "peso": perfil.peso,
        "deporte": perfil.deporte,
        "id_entrenador": perfil.id_entrenador,
        "frecuencia_cardiaca_minima": perfil.frecuencia_cardiaca_minima,
        "frecuencia_cardiaca_maxima": perfil.frecuencia_cardiaca_maxima
    }

#Eliminar un atleta
@router.delete("/{atleta_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_atleta(atleta_id: int, db: Session = Depends(get_db)):
    """Elimina un atleta por ID de perfil (id_atleta)"""
    # Primero buscar el perfil
    perfil = db.query(models.PerfilAtleta).filter_by(id_atleta=atleta_id).first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil de atleta no encontrado")
    
    # Luego eliminar en orden correcto (primero perfil, luego usuario)
    db.query(models.PerfilAtleta).filter_by(id_atleta=atleta_id).delete()
    db.query(models.Usuario).filter_by(id_usuario=perfil.id_usuario).delete()
    db.commit()
    
    return None


