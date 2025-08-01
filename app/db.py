from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ⚠️ SOLO PARA PRUEBAS. NO SUBIR A PRODUCCIÓN.
DATABASE_URL = "mysql+pymysql://root:qRpSTZzgOjdULHQYHkSQofFaeMZEsgWQ@interchange.proxy.rlwy.net:19565/railway"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
