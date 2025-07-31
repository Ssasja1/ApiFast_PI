from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas
from app.models import PerfilAtleta, Entrenador, Entrenamiento
from app.schemas import PerfilAtletaDashboardResponse, EntrenamientoSchema, AtletaOut, AtletaUpdateSchema


router = APIRouter(prefix="/atletas", tags=["Atleta Dashboard"])

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

#✅ NUEVA RUTA: Obtener atleta por id_usuario (para login)
@router.get("/usuario/{id_usuario}", response_model=AtletaOut)
def get_atleta_by_usuario(id_usuario: int, db: Session = Depends(get_db)):
     atleta = db.query(PerfilAtleta).filter(PerfilAtleta.id_usuario == id_usuario).first()
     if not atleta:
         raise HTTPException(status_code=404, detail="Perfil de atleta no encontrado")
     return atleta


#GET (Obtener un atleta por ID)
@router.get("/perfil/{atleta_id}", response_model=schemas.AtletaResponse)
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


#quien sabe
#GET (Obtener un atleta por ID)
