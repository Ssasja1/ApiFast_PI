from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db import get_db
from app.models import PerfilEntrenador, Entrenamiento, PerfilAtleta, AsignacionAtleta
from app.schemas import (
    CoachOut,
    EntrenamientoOut,
    PostEntrenamiento as PostEntrenamientoSchema,
    AsignacionCreate,
    AsignacionResponse,
    AtletaOut,
)

router = APIRouter(prefix="/coaches", tags=["Coaches"])


@router.get("/{id_usuario}", response_model=CoachOut)
def get_coach_dashboard(id_usuario: int, db: Session = Depends(get_db)):
    coach = db.query(PerfilEntrenador).filter(PerfilEntrenador.id_usuario == id_usuario).first()
    if not coach:
        raise HTTPException(status_code=404, detail="Coach no encontrado")

    atletas = db.query(PerfilAtleta).filter(PerfilAtleta.id_entrenador == coach.id_entrenador).all()

    # Usar from_orm para convertir cada atleta a AtletaOut
    atletas_asignados = [AtletaOut.from_orm(a) for a in atletas]

    return {
        "id_entrenador": coach.id_entrenador,
        "nombre_completo": coach.nombre_completo,
        "fecha_nacimiento": coach.fecha_nacimiento,
        "especialidad": coach.especialidad,
        "experiencia": coach.experiencia,
        "atletas_asignados": atletas_asignados,
    }


@router.get("/{id_entrenador}/atletas", response_model=List[AtletaOut])
def get_atletas_by_entrenador(id_entrenador: int, db: Session = Depends(get_db)):
    atletas = db.query(PerfilAtleta).filter(PerfilAtleta.id_entrenador == id_entrenador).all()
    if not atletas:
        raise HTTPException(status_code=404, detail="No se encontraron atletas para este entrenador")
    return atletas  # FastAPI los convierte automáticamente gracias a orm_mode


@router.post("/entrenamientos")
def crear_entrenamiento(data: PostEntrenamientoSchema, db: Session = Depends(get_db)):
    nuevo = Entrenamiento(
        id_entrenador=data.id_entrenador,
        titulo=data.titulo,
        descripcion=data.descripcion,
        duracion_estimada=data.duracion_estimada,
        nivel_dificultad=data.nivel_dificultad,
        fecha_creacion=datetime.now()
    )

    try:
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return {"mensaje": "Entrenamiento creado", "id_entrenamiento": nuevo.id_entrenamiento}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear entrenamiento: {e}")


@router.get("/entrenamientos/coach/{id_entrenador}", response_model=List[EntrenamientoOut])
def get_entrenamientos_by_coach(id_entrenador: int, db: Session = Depends(get_db)):
    entrenamientos = db.query(Entrenamiento).filter(Entrenamiento.id_entrenador == id_entrenador).all()
    return entrenamientos


@router.get("/entrenamientos/{id_entrenamiento}", response_model=EntrenamientoOut)
def get_entrenamiento_by_id(id_entrenamiento: int, db: Session = Depends(get_db)):
    entrenamiento = db.query(Entrenamiento).filter(Entrenamiento.id_entrenamiento == id_entrenamiento).first()
    if not entrenamiento:
        raise HTTPException(status_code=404, detail="Entrenamiento no encontrado")
    return entrenamiento


@router.put("/entrenamientos/{id_entrenamiento}")
def update_entrenamiento(id_entrenamiento: int, data: PostEntrenamientoSchema, db: Session = Depends(get_db)):
    entrenamiento = db.query(Entrenamiento).filter(Entrenamiento.id_entrenamiento == id_entrenamiento).first()
    if not entrenamiento:
        raise HTTPException(status_code=404, detail="Entrenamiento no encontrado")

    entrenamiento.titulo = data.titulo
    entrenamiento.descripcion = data.descripcion
    entrenamiento.duracion_estimada = data.duracion_estimada
    entrenamiento.nivel_dificultad = data.nivel_dificultad

    try:
        db.commit()
        return {"mensaje": "Entrenamiento actualizado correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar: {e}")


@router.post("/asignaciones", response_model=AsignacionResponse)
def asignar_entrenamiento(data: AsignacionCreate, db: Session = Depends(get_db)):
    # Validar que el entrenamiento y el atleta existan
    entrenamiento = db.query(Entrenamiento).filter_by(id_entrenamiento=data.id_entrenamiento).first()
    if not entrenamiento:
        raise HTTPException(status_code=404, detail="Entrenamiento no encontrado")

    atleta = db.query(PerfilAtleta).filter_by(id_atleta=data.id_atleta).first()
    if not atleta:
        raise HTTPException(status_code=404, detail="Atleta no encontrado")

    # Crear asignación
    asignacion = AsignacionAtleta(
        id_entrenamiento=data.id_entrenamiento,
        id_atleta=data.id_atleta,
        estado="pendiente"
    )
    db.add(asignacion)
    db.commit()
    db.refresh(asignacion)

    return asignacion