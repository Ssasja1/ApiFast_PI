from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import atleta, entrenador, register  # 👈 Importa también register
from app.routes import auth
from app.routes import atletas_dashboard
from app.routes import coach_dashboard



app = FastAPI(
    title="API PI",
    description="API creada para la aplicación móvil del PI",
    version="1.0.0"
)

# Configuración CORS para aceptar peticiones desde tu app móvil o localhost (ajusta la URL si usas producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Reemplaza "*" por tus orígenes reales en producción
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)

# Incluir las rutas
app.include_router(atleta.router)
app.include_router(entrenador.router)
app.include_router(register.router) 
app.include_router(auth.router)
app.include_router(atletas_dashboard.router)
app.include_router(coach_dashboard.router)
