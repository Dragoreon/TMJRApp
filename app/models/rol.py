from pydantic import BaseModel

# Ir aquí por si hay que hacer algo con ENUM 
# https://fastapi.tiangolo.com/tutorial/path-params/#declare-a-path-parameter

class Rol(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None

class RolUpdate(Rol):
    nombre: str | None = None