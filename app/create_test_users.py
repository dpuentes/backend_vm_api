from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import User
from passlib.context import CryptContext
from .schemas import Role

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_test_users():
    # Crear una sesión de base de datos
    db = SessionLocal()

    # Lista de usuarios de prueba
    test_users = [
        {
            "email": "admin@example.com",
            "username": "admin",
            "password": "admin123",
            "is_superuser": True,
            "role": Role.ADMIN
        },
        {
            "email": "user1@example.com",
            "username": "user1",
            "password": "user123",
            "is_superuser": False,
            "role": Role.CLIENT
        },
        {
            "email": "user2@example.com",
            "username": "user2",
            "password": "user123",
            "is_superuser": False,
            "role": Role.CLIENT
        }
    ]

    try:
        for user_data in test_users:
            # Verificar si el usuario ya existe
            existing_user = db.query(User).filter(
                (User.email == user_data["email"]) |
                (User.username == user_data["username"])
            ).first()

            if not existing_user:
                # Crear nuevo usuario
                hashed_password = pwd_context.hash(user_data["password"])
                new_user = User(
                    email=user_data["email"],
                    username=user_data["username"],
                    hashed_password=hashed_password,
                    is_superuser=user_data["is_superuser"],
                    role=user_data["role"]
                )
                db.add(new_user)
                print(f"Usuario creado: {user_data['username']}")
            else:
                print(f"Usuario ya existe: {user_data['username']}")

        db.commit()
        print("Proceso completado exitosamente")

    except Exception as e:
        db.rollback()
        print(f"Error al crear usuarios: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_users()