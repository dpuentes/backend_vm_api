from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine, get_db
from .routers import users, virtual_machine

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="VM API",
    description="API para gestión de máquinas virtuales",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(virtual_machine.router, prefix="/api/v1/virtual-machines", tags=["virtual-machines"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Gestión de Máquinas Virtuales"}
