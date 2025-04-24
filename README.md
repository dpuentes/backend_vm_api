# Backend VM API

API REST para la gestión de máquinas virtuales desarrollada con FastAPI.

## 🚀 Características

- Autenticación JWT
- Gestión de usuarios y roles (ADMIN y CLIENT)
- Operaciones CRUD para máquinas virtuales
- Base de datos PostgreSQL
- Documentación automática de la API
- Despliegue en Render

## 📋 Prerrequisitos

- Python 3.8+
- PostgreSQL
- Git

## 🔧 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/dpuentes/backend_vm_api.git
cd backend_vm_api
```

2. Crear y activar un entorno virtual:
```bash
python -m venv env
source env/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:
```env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_db
SECRET_KEY=tu_clave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🏃‍♂️ Ejecución

1. Iniciar la base de datos PostgreSQL

2. Ejecutar la aplicación:
```bash
uvicorn app.main:app --reload
```

La aplicación estará disponible en `http://localhost:8000`

## 👥 Creación de Usuarios

La API soporta dos tipos de roles: ADMIN y CLIENT. Para crear usuarios, puedes usar el endpoint de creación con los siguientes ejemplos:

### Usuario Administrador
```json
{
    "email": "admin@example.com",
    "username": "admin",
    "password": "admin123",
    "is_superuser": true,
    "role": "ADMIN"
}
```

### Usuario Cliente
```json
{
    "email": "user1@example.com",
    "username": "user1",
    "password": "user123",
    "is_superuser": false,
    "role": "CLIENT"
}
```

## 📚 Documentación de la API

Una vez ejecutada la aplicación, puedes acceder a:
- Documentación Swagger UI: `http://localhost:8000/docs`
- Documentación ReDoc: `http://localhost:8000/redoc`

## 🧪 Testing

Para ejecutar las pruebas:
```bash
pytest
```

## 🛠 Estructura del Proyecto

```
backend_vm_api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── crud.py
│   ├── database.py
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── users.py
│       └── virtual_machine.py
├── tests/
├── frontend/
├── requirements.txt
├── .env
└── README.md
```

## 🔐 Autenticación

La API utiliza JWT para autenticación. Para acceder a los endpoints protegidos:
1. Obtener token: POST `/token`
2. Incluir token en el header: `Authorization: Bearer <token>`

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📞 Contacto

Diego Puentes - [@dpuentes](https://github.com/dpuentes) - dipuentes123@gmail.com

Project Link: [https://github.com/dpuentes/backend_vm_api](https://github.com/dpuentes/backend_vm_api)