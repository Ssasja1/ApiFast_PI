from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean, ForeignKey, DECIMAL, Date, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base

class Usuario(Base):
    __tablename__ = 'usuarios'

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    contrasena_hash = Column(String(255), nullable=False)
    tipo = Column(Enum('atleta', 'entrenador', 'administrador'), nullable=False)
    fecha_registro = Column(DateTime, server_default=func.now())
    ultimo_login = Column(DateTime, nullable=True)
    activo = Column(Boolean, default=True)

class PerfilAtleta(Base):
    __tablename__ = 'perfiles_atletas'

    id_atleta = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    nombre_completo = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    altura = Column(DECIMAL(5, 2), nullable=True)
    peso = Column(DECIMAL(5, 2), nullable=True)
    deporte = Column(String(50), nullable=False)
    id_entrenador = Column(Integer, ForeignKey('entrenadores.id_entrenador'), nullable=True)
    frecuencia_cardiaca_maxima = Column(Integer, nullable=True)
    frecuencia_cardiaca_minima = Column(Integer, nullable=True)

    entrenador = relationship("Entrenador", back_populates="atletas")
    asignaciones = relationship("AsignacionAtleta", back_populates="atleta", cascade="all, delete-orphan")
    # ❌ Eliminar esta relación porque ya no hay campo id_atleta en entrenamientos
    # entrenamientos = relationship("Entrenamiento", back_populates="atleta")

class Entrenador(Base):
    __tablename__ = "entrenadores"

    id_entrenador = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))

    atletas = relationship("PerfilAtleta", back_populates="entrenador")
    entrenamientos = relationship("Entrenamiento", back_populates="entrenador")

class Entrenamiento(Base):
    __tablename__ = "entrenamientos"

    id_entrenamiento = Column(Integer, primary_key=True, index=True)
    id_entrenador = Column(Integer, ForeignKey("entrenadores.id_entrenador"), nullable=False)
    # ❌ Eliminar esta línea completamente:
    # id_atleta = Column(Integer, ForeignKey("perfiles_atletas.id_atleta"), nullable=True)

    titulo = Column(String(100), nullable=False)
    descripcion = Column(Text)
    duracion_estimada = Column(Integer)
    fecha_creacion = Column(DateTime)
    nivel_dificultad = Column(Enum("principiante", "intermedio", "avanzado"))

    entrenador = relationship("Entrenador", back_populates="entrenamientos")
    # ❌ Eliminar esta relación también:
    # atleta = relationship("PerfilAtleta", back_populates="entrenamientos")
    asignaciones = relationship("AsignacionAtleta", back_populates="entrenamiento", cascade="all, delete-orphan")

class PerfilEntrenador(Base):
    __tablename__ = 'perfiles_entrenadores'

    id_entrenador = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'), nullable=False)
    nombre_completo = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    especialidad = Column(String(50), nullable=True)
    experiencia = Column(Text, nullable=True)

class AsignacionAtleta(Base):
    __tablename__ = "asignaciones_atletas"

    id_asignacion = Column(Integer, primary_key=True, autoincrement=True)
    id_entrenamiento = Column(Integer, ForeignKey("entrenamientos.id_entrenamiento"), nullable=False)
    id_atleta = Column(Integer, ForeignKey("perfiles_atletas.id_atleta"), nullable=False)

    fecha_asignacion = Column(Date, nullable=False)
    fecha_completado = Column(Date, nullable=True)
    estado = Column(Enum("pendiente", "en_progreso", "completado"), nullable=False, default="pendiente")
    feedback = Column(Text, nullable=True)
    calificacion = Column(Integer, nullable=True)

    atleta = relationship("PerfilAtleta", back_populates="asignaciones")
    entrenamiento = relationship("Entrenamiento", back_populates="asignaciones")

