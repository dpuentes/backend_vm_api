# Documentación de Arquitectura - Backend VM API

## 1. Visión General

La aplicación es una API REST desarrollada con FastAPI para la gestión de máquinas virtuales. Sigue una arquitectura de capas bien definida y utiliza patrones de diseño modernos para asegurar escalabilidad y mantenibilidad.

## 2. Arquitectura del Sistema

### 2.1 Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                      Cliente HTTP                        │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│                      FastAPI Server                      │
└───────────────┬───────────────┬───────────────┬─────────┘
                │               │               │
┌───────────────▼───┐   ┌───────▼──────┐   ┌───▼───────────┐
│    Routers        │   │  Servicios   │   │  Modelos      │
│  (Controladores)  │   │  (Lógica de  │   │  (Datos)      │
└───────────────┬───┘   │  Negocio)    │   └───────┬───────┘
                │       └───────┬──────┘           │
                │               │                   │
┌───────────────▼───────────────▼───────────────────▼───────┐
│                      Base de Datos                         │
│                      PostgreSQL                            │
└───────────────────────────────────────────────────────────┘
```

### 2.2 Capas de la Aplicación

1. **Capa de Presentación (API)**
   - `app/main.py`: Punto de entrada de la aplicación
   - `app/routers/`: Endpoints de la API
     - `auth.py`: Autenticación y autorización
     - `users.py`: Gestión de usuarios
     - `virtual_machine.py`: Gestión de VMs

2. **Capa de Servicios**
   - `app/auth.py`: Lógica de autenticación JWT
   - `app/crud.py`: Operaciones CRUD genéricas
   - `app/database.py`: Configuración de la base de datos

3. **Capa de Modelos**
   - `app/models.py`: Modelos SQLAlchemy
   - `app/schemas.py`: Esquemas Pydantic

## 3. Componentes Principales

### 3.1 Autenticación y Autorización

```python
# app/auth.py
class AuthHandler:
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def create_access_token(self, data: dict) -> str:
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
```

Características clave:
- Implementación de JWT para autenticación
- Hashing de contraseñas con bcrypt
- Sistema de roles (ADMIN/CLIENT)
- Middleware de verificación de tokens

### 3.2 Gestión de Usuarios

```python
# app/models.py
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
    is_superuser = Column(Boolean, default=False)
```

Características:
- Modelo de usuario con roles
- Validación de datos con Pydantic
- Operaciones CRUD completas
- Gestión de permisos basada en roles

### 3.3 Gestión de Máquinas Virtuales

```python
# app/models.py
class VirtualMachine(Base):
    __tablename__ = "virtual_machines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cores = Column(Integer)
    ram = Column(Integer)
    disk = Column(Integer)
    os = Column(String)
    status = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
```

Características:
- Modelo completo de máquina virtual
- Relaciones con usuarios
- Validación de estados y recursos
- Control de acceso basado en roles

## 4. Patrones de Diseño

### 4.1 Repository Pattern
```python
# app/crud.py
class CRUDBase:
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
```

### 4.2 Dependency Injection
```python
# app/database.py
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## 5. Seguridad

### 5.1 Autenticación
- JWT con expiración configurable
- Hashing de contraseñas con bcrypt
- Protección contra ataques de fuerza bruta

### 5.2 Autorización
- Sistema de roles (ADMIN/CLIENT)
- Middleware de verificación de permisos
- Validación de datos de entrada

## 6. Base de Datos

### 6.1 Estructura
- PostgreSQL como motor principal
- SQLAlchemy como ORM
- Migraciones automáticas

### 6.2 Relaciones
- Usuarios -> Máquinas Virtuales (1:N)
- Roles -> Permisos (1:N)

### 6.3 Diagrama ERD

```
┌─────────────────────────────────────────────────────────────────┐
│                           users                                  │
├─────────────────────────────────────────────────────────────────┤
│ PK | id                | SERIAL                                  │
│    | email            | VARCHAR(255) UNIQUE NOT NULL            │
│    | username         | VARCHAR(255) UNIQUE NOT NULL            │
│    | hashed_password  | VARCHAR(255) NOT NULL                   │
│    | role            | VARCHAR(50) NOT NULL                     │
│    | is_superuser    | BOOLEAN DEFAULT FALSE                    │
│    | created_at      | TIMESTAMP WITH TIME ZONE DEFAULT NOW()   │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                │ 1:N
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                      virtual_machines                           │
├─────────────────────────────────────────────────────────────────┤
│ PK | id                | SERIAL                                  │
│ FK | owner_id         | INTEGER REFERENCES users(id)            │
│    | name             | VARCHAR(255) NOT NULL                   │
│    | cores            | INTEGER NOT NULL                        │
│    | ram              | INTEGER NOT NULL                        │
│    | disk             | INTEGER NOT NULL                        │
│    | os               | VARCHAR(100) NOT NULL                   │
│    | status           | VARCHAR(50) NOT NULL                    │
│    | created_at       | TIMESTAMP WITH TIME ZONE DEFAULT NOW()  │
│    | updated_at       | TIMESTAMP WITH TIME ZONE                │
└─────────────────────────────────────────────────────────────────┘

Leyenda:
PK = Primary Key
FK = Foreign Key
```

Descripción de las tablas:

1. **users**
   - Almacena información de usuarios del sistema
   - Campos principales: email, username, hashed_password
   - Campos de control: role, is_superuser
   - Timestamps: created_at

2. **virtual_machines**
   - Almacena información de máquinas virtuales
   - Relación con users a través de owner_id
   - Campos de recursos: cores, ram, disk
   - Campos de configuración: os, status
   - Timestamps: created_at, updated_at

Relaciones:
- Un usuario puede tener múltiples máquinas virtuales (1:N)
- Cada máquina virtual pertenece a un único usuario
- La eliminación de un usuario puede estar restringida si tiene máquinas virtuales asociadas

## 7. API REST

### 7.1 Endpoints Principales
```
POST   /api/v1/login
POST   /api/v1/users/
GET    /api/v1/users/me
GET    /api/v1/users/
POST   /api/v1/virtual-machines/
GET    /api/v1/virtual-machines/
GET    /api/v1/virtual-machines/{vm_id}
PUT    /api/v1/virtual-machines/{vm_id}
DELETE /api/v1/virtual-machines/{vm_id}
```

### 7.2 Documentación
- Swagger UI integrado
- Esquemas OpenAPI
- Documentación automática

## 8. Consideraciones de Despliegue

### 8.1 Configuración
- Variables de entorno
- Configuración de base de datos
- Claves de seguridad

### 8.2 Escalabilidad
- Diseño stateless
- Conexiones a base de datos pool
- Caché de tokens

## 9. Mejores Prácticas Implementadas

1. **Código Limpio**
   - Nombres descriptivos
   - Funciones pequeñas y específicas
   - Documentación clara

2. **Seguridad**
   - Validación de datos
   - Protección contra inyección SQL
   - Manejo seguro de contraseñas

3. **Mantenibilidad**
   - Separación de responsabilidades
   - Patrones de diseño establecidos
   - Testing automatizado

## 10. Áreas de Mejora Potencial

1. Implementación de caché
2. Sistema de logging más robusto
3. Monitoreo y métricas
4. Documentación de API más detallada
5. Implementación de rate limiting