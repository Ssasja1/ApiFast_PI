import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Usa la URL de Railway
DATABASE_URL = os.getenv("MYSQL_URL")  # Railway define esta variable automáticamente

if not DATABASE_URL:
    raise ValueError("MYSQL_URL no está definida. Verifica tus variables de entorno en Railway.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
