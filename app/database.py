from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener DATABASE_URL de las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Si no existe DATABASE_URL, usar las variables individuales
if not DATABASE_URL:
    POSTGRES_USER = os.getenv("POSTGRES_USER", "vm_api_user_db")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "root12345")
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "vm_api_db")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Render usa postgres:// pero SQLAlchemy necesita postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency para manejar sesiones de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()