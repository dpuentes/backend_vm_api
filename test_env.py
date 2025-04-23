from dotenv import load_dotenv
import os

# Cargar las variables de entorno
load_dotenv()

# Imprimir las variables de entorno
print("=== Configuración de Base de Datos ===")
print(f"Usuario: {os.getenv('POSTGRES_USER')}")
print(f"Base de datos: {os.getenv('POSTGRES_DB')}")
print(f"Servidor: {os.getenv('POSTGRES_SERVER')}")
print(f"Puerto: {os.getenv('POSTGRES_PORT')}")

print("\n=== Configuración de JWT ===")
print(f"Algoritmo: {os.getenv('ALGORITHM')}")
print(f"Tiempo de expiración: {os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')} minutos")

print("\n=== Configuración de la Aplicación ===")
print(f"Entorno: {os.getenv('ENVIRONMENT')}")
print(f"Debug: {os.getenv('DEBUG')}")