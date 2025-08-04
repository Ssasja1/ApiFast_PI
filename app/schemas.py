from pydantic import BaseModel, EmailStr, constr
from datetime import date, datetime  
from typing import Optional, Literal, List
from enum import Enum

class UsuarioBase(BaseModel):
    id_usuario: int
    email: EmailStr
    tipo: str

    class Config:
        orm_mode = True
        from_attributes = True

class EstadoAsignacion(str, Enum):
    pendiente = "pendiente"
    en_progreso = "en_progreso"
    completado = "completado"

class AsignacionCreate(BaseModel):
    id_entrenamiento: int
    id_atleta: int

class AsignacionResponse(BaseModel):
    id_asignacion: int
    id_entrenamiento: int
    id_atleta: int
    fecha_asignacion: Optional[date]
    fecha_completado: Optional[date]
    estado: EstadoAsignacion
    feedback: Optional[str]
    calificacion: Optional[int]

    class Config:
        orm_mode = True


class AtletaCreate(BaseModel):
    email: EmailStr
    contrasena: constr(min_length=6)
    nombre_completo: str
    fecha_nacimiento: date
    altura: Optional[float] = None  # Cambio clave
    peso: Optional[float] = None    # Cambio clave
    deporte: str
    id_entrenador: Optional[int] = None  # Cambio clave (solución principal)
    frecuencia_cardiaca_minima: Optional[int] = None  # Cambio clave

class EntrenamientoAsignadoResponse(BaseModel):
    id_entrenamiento: int
    titulo: str
    descripcion: Optional[str]
    duracion_estimada: Optional[int]
    nivel_dificultad: Optional[str]

    class Config:
        from_attributes = True

class AsignacionAtletaResponse(BaseModel):
    id_asignacion: int
    fecha_asignacion: Optional[date] = None
    fecha_completado: Optional[date] = None
    estado: EstadoAsignacion
    feedback: Optional[str]
    calificacion: Optional[int]
    entrenamiento: Optional[EntrenamientoAsignadoResponse] = None  # Puede ser None si no hay entrenamiento asignado

    class Config:
        from_attributes = True
class AtletaResponse(BaseModel):
    id_atleta: int  # 
    usuario: UsuarioBase  # Relación con Usuario
    email: EmailStr
    tipo: str
    nombre_completo: str
    fecha_nacimiento: date  # Nuevo campo
    altura: Optional[float]  # Nuevo campo
    peso: Optional[float]    # Nuevo campo
    deporte: str
    id_entrenador: Optional[int]  # Nuevo campo
    frecuencia_cardiaca_minima: Optional[int]  # Nuevo campo
    frecuencia_cardiaca_maxima: Optional[int]  # Nuevo campo
    asignaciones: List[AsignacionAtletaResponse]

    class Config:
        from_attributes = True

# En schemas.py
class AtletaUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    altura: Optional[float] = None
    peso: Optional[float] = None
    deporte: Optional[str] = None
    id_entrenador: Optional[int] = None
    frecuencia_cardiaca_minima: Optional[int] = None




class EntrenadorCreate(BaseModel):
    email: EmailStr
    contrasena: constr(min_length=6)
    nombre_completo: str
    fecha_nacimiento: date
    especialidad: str
    experiencia: str

class EntrenadorUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    especialidad: Optional[str] = None
    experiencia: Optional[str] = None

class EntrenadorResponse(BaseModel):
    id_entrenador: int
    id_usuario: int
    email: str
    tipo: str
    nombre_completo: str
    fecha_nacimiento: Optional[date] = None  # Hacer opcional
    especialidad: Optional[str] = None       # Hacer opcional
    experiencia: Optional[str] = None        # Hacer opcional (solución clave)
    fecha_registro: datetime
    activo: bool
    atletas_asignados: List[int] = []  # Lista de IDs de atletas asignados
    
    class Config:
        from_attributes = True

#schemas nuevos
class RegistroUsuario(BaseModel):
    email: EmailStr
    contrasena: str
    tipo: Literal["atleta", "entrenador"]
    nombre_completo: str
    fecha_nacimiento: date

    # Campos para atleta
    altura: Optional[float] = None
    peso: Optional[float] = None
    deporte: Optional[str] = None
    frecuencia_cardiaca_minima: Optional[int] = None
    id_entrenador: Optional[int] = None

    # Campos para entrenador
    especialidad: Optional[str] = None
    experiencia: Optional[str] = None

#nuevos sisisi
class EntrenamientoSchema(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str]
    duracion: Optional[int]
    fecha_creacion: Optional[datetime]
    dificultad: Optional[str]
    estado: str = "pendiente"  # por defecto

    class Config:
        from_attributes = True  # si usas SQLAlchemy 2.0 o más reciente

class PerfilAtletaDashboardResponse(BaseModel):
    id_atleta: int
    id_usuario: int
    nombre_completo: str
    fecha_nacimiento: date
    altura: Optional[float]
    peso: Optional[float]
    deporte: str
    frecuencia_cardiaca_maxima: Optional[int]
    frecuencia_cardiaca_minima: Optional[int]
    nombre_entrenador: Optional[str]
    entrenamientos: List[EntrenamientoSchema]

    class Config:
        from_attributes = True

# Debe estar en app/schemas.py

class AtletaOut(BaseModel):
    id_atleta: int
    id_usuario: int
    nombre_completo: str
    fecha_nacimiento: date
    altura: Optional[float]
    peso: Optional[float]
    deporte: str
    frecuencia_cardiaca_maxima: Optional[int]
    frecuencia_cardiaca_minima: Optional[int]

    class Config:
        from_attributes = True

class AtletaUpdateSchema(BaseModel):
    nombre_completo: Optional[str]
    fecha_nacimiento: Optional[date]
    altura: Optional[float]
    peso: Optional[float]
    deporte: Optional[str]
    frecuencia_cardiaca_minima: Optional[int]
    frecuencia_cardiaca_maxima: Optional[int]
    id_entrenador: Optional[int] = None

    class Config:
        orm_mode = True

class CoachOut(BaseModel):
    id_entrenador: int
    nombre_completo: str
    fecha_nacimiento: Optional[date]
    especialidad: Optional[str]
    experiencia: Optional[str]
    atletas_asignados: List[AtletaOut]  # Lista de diccionarios con datos de atletas asignados

    class Config:
        orm_mode = True


class NivelDificultad(str, Enum):
    principiante = "principiante"
    intermedio = "intermedio"
    avanzado = "avanzado"

class PostEntrenamiento(BaseModel):  # ✅ Este es solo para recibir datos
    id_entrenador: int
    titulo: str
    descripcion: Optional[str] = None
    duracion_estimada: int
    nivel_dificultad: NivelDificultad

    class Config:
        orm_mode = True


class EntrenamientoOut(BaseModel):
    id_entrenamiento: int
    id_entrenador: int  # ✅ NECESARIO
    titulo: str
    descripcion: Optional[str]
    duracion_estimada: Optional[int]
    nivel_dificultad: Optional[str]
    fecha_creacion: Optional[datetime]

    class Config:
        orm_mode = True