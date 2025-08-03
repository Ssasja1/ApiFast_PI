from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import atleta, entrenador, register, auth, atletas_dashboard, coach_dashboard
from app.db import engine, Base  # 👈 Importar Base y engine
from app import models  # 👈 Importar los modelos para registrarlos

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API PI",
    description="API creada para la aplicación móvil del PI",
    version="1.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas
app.include_router(atleta.router)
app.include_router(entrenador.router)
app.include_router(register.router)
app.include_router(auth.router)
app.include_router(atletas_dashboard.router)
app.include_router(coach_dashboard.router)
