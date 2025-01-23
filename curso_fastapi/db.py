### En este archivo se observa la lógica necesaria para la conexión con la base de datos
from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import create_engine, Session
from sqlmodel import SQLModel

# URL de conexión a PostgreSQL (ajusta con tus datos)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:h7T-3=aB@localhost:5432/course_fastapi" #Se modifica en función a la db

# Crear el motor de base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)#, echo=True)

# Crear una sesión
def get_session():
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)]

# Crear las tablas si no existen
def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
