from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import PerfilEntrenador
from app.schemas import CoachOut  # Asegúrate de tener este schema definido

router = APIRouter(prefix="/coaches", tags=["Coaches"])

@router.get("/{id_usuario}", response_model=CoachOut)
def get_coach_dashboard(id_usuario: int, db: Session = Depends(get_db)):
    coach = db.query(PerfilEntrenador).filter(PerfilEntrenador.id_usuario == id_usuario).first()

    if not coach:
        raise HTTPException(status_code=404, detail="Coach no encontrado")

    return coach
