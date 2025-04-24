from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
POSTGRES_USER = os.getenv("POSTGRES_USER", "vm_api_user_db")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "root12345")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "vm_api_db")

# Si existe DATABASE_URL (usado por Render), úsalo en lugar de construir la URL
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    # Render usa postgres:// pero SQLAlchemy necesita postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URL = DATABASE_URL
else:
    SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency para manejar sesiones de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()