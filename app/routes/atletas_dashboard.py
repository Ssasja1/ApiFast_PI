from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import PerfilAtleta, Entrenador, Entrenamiento
from app.schemas import PerfilAtletaDashboardResponse, EntrenamientoSchema, AtletaOut, AtletaUpdateSchema


router = APIRouter(prefix="/atletas", tags=["Atletas"])

# Dashboard detallado por ID de usuario
@router.get("/{id_usuario}", response_model=PerfilAtletaDashboardResponse)
def get_atleta_dashboard(id_usuario: int, db: Session = Depends(get_db)):
    atleta = db.query(PerfilAtleta).filter(PerfilAtleta.id_usuario == id_usuario).first()

    if not atleta:
        raise HTTPException(status_code=404, detail="Atleta no encontrado")

    nombre_entrenador = None
    if atleta.id_entrenador:
        entrenador = db.query(Entrenador).filter(Entrenador.id_entrenador == atleta.id_entrenador).first()
        if entrenador:
            nombre_entrenador = entrenador.nombre_completo

    entrenamientos = []
    if atleta.id_entrenador:
        entrenamientos_db = db.query(Entrenamiento).filter(Entrenamiento.id_entrenador == atleta.id_entrenador).all()
        entrenamientos = [
            EntrenamientoSchema(
                id=e.id_entrenamiento,
                titulo=e.titulo,
                descripcion=e.descripcion,
                duracion=e.duracion_estimada,
                fecha_creacion=e.fecha_creacion,
                dificultad=e.nivel_dificultad,
                estado="pendiente"
            ) for e in entrenamientos_db
        ]

    return {
        "id_atleta": atleta.id_atleta,
        "id_usuario": atleta.id_usuario,
        "nombre_completo": atleta.nombre_completo,
        "fecha_nacimiento": atleta.fecha_nacimiento,
        "altura": atleta.altura,
        "peso": atleta.peso,
        "deporte": atleta.deporte,
        "frecuencia_cardiaca_minima": atleta.frecuencia_cardiaca_minima,
        "frecuencia_cardiaca_maxima": atleta.frecuencia_cardiaca_maxima,
        "nombre_entrenador": nombre_entrenador,
        "entrenamientos": entrenamientos
    }


# Datos básicos por id_atleta (opcional)
@router.get("/basico/{atleta_id}", response_model=AtletaOut)
def get_atleta_by_id(atleta_id: int, db: Session = Depends(get_db)):
    atleta = db.query(PerfilAtleta).filter(PerfilAtleta.id_atleta == atleta_id).first()
    if not atleta:
        raise HTTPException(status_code=404, detail="Atleta no encontradoooooo")
    return atleta

# ✅ NUEVA RUTA: Obtener atleta por id_usuario (para login)
@router.get("/usuario/{id_usuario}", response_model=AtletaOut)
def get_atleta_by_usuario(id_usuario: int, db: Session = Depends(get_db)):
    atleta = db.query(PerfilAtleta).filter(PerfilAtleta.id_usuario == id_usuario).first()
    if not atleta:
        raise HTTPException(status_code=404, detail="Perfil de atleta no encontrado")
    return atleta

@router.put("/editar/{id_atleta}")
def actualizar_atleta(id_atleta: int, atleta_data: AtletaUpdateSchema, db: Session = Depends(get_db)):
    atleta = db.query(PerfilAtleta).filter(PerfilAtleta.id_atleta == id_atleta).first()

    if not atleta:
        raise HTTPException(status_code=404, detail="Atleta no encontrado")

    for key, value in atleta_data.dict(exclude_unset=True).items():
        setattr(atleta, key, value)

    db.commit()
    db.refresh(atleta)

    return {"mensaje": "Perfil actualizado correctamente", "atleta": atleta}