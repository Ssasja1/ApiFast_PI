from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import PerfilEntrenador, Entrenamiento  # ✅ solo importas modelos reales aquí
from app.schemas import CoachOut, EntrenamientoOut, PostEntrenamiento as PostEntrenamientoSchema  # ✅ Pydantic schema
from datetime import datetime


router = APIRouter(prefix="/coaches", tags=["Coaches"])


@router.get("/{id_usuario}", response_model=CoachOut)
def get_coach_dashboard(id_usuario: int, db: Session = Depends(get_db)):
    coach = db.query(PerfilEntrenador).filter(PerfilEntrenador.id_usuario == id_usuario).first()

    if not coach:
        raise HTTPException(status_code=404, detail="Coach no encontrado")

    return coach

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

@router.get("/entrenamientos/coach/{id_entrenador}", response_model=list[EntrenamientoOut])
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
