from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session
from fastapi import Depends

# Usa la URL directamente (sin .env)
DATABASE_URL = "mysql://root:qRpSTZzgOjdULHQYHkSQofFaeMZEsgWQ@interchange.proxy.rlwy.net:19565/railway"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# 👉 Esta es la función que te faltaba
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
