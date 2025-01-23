from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

# Definir el modelo de entrada con Pydantic
class FilterParams(BaseModel):
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    precio_min: Optional[float] = None
    precio_max: Optional[float] = None

# Definir el modelo de salida con Pydantic
class Producto(BaseModel):
    id: int
    nombre: str
    categoria: str
    precio: float

# Crear la aplicación FastAPI
app = FastAPI()

# Base de datos simulada (una lista de productos)
productos_db = [
    Producto(id=1, nombre="Producto 1", categoria="Electrónica", precio=100),
    Producto(id=2, nombre="Producto 2", categoria="Electrónica", precio=200),
    Producto(id=3, nombre="Producto 3", categoria="Hogar", precio=50),
    Producto(id=4, nombre="Producto 4", categoria="Hogar", precio=150),
    Producto(id=5, nombre="Producto 5", categoria="Deportes", precio=75)
]



# Endpoint POST para filtrar productos
@app.post("/productos", response_model=List[Producto])
def filtrar_productos(filtro: FilterParams):
    # Filtrar productos según los parámetros proporcionados
    resultados = productos_db

    if filtro.nombre:
        resultados = [producto for producto in resultados if filtro.nombre.lower() in producto.nombre.lower()]

    if filtro.categoria:
        resultados = [producto for producto in resultados if filtro.categoria.lower() in producto.categoria.lower()]

    if filtro.precio_min is not None:
        resultados = [producto for producto in resultados if producto.precio >= filtro.precio_min]

    if filtro.precio_max is not None:
        resultados = [producto for producto in resultados if producto.precio <= filtro.precio_max]

    return resultados