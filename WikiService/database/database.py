import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Carga las variables de .env al entorno
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# El "engine" es la conexión real a Neon
engine = create_engine(DATABASE_URL)

# Cada request va a pedir su propia "sesión" de conversación con la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de la que van a heredar todos tus modelos (models.py)
Base = declarative_base()

# Esta función se la vamos a pasar a FastAPI como "dependencia":
# abre una sesión, se la presta al endpoint, y la cierra sola al terminar
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()