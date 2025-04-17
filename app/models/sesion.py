from pydantic import BaseModel

class Sesion(BaseModel):
    id: int
    id_aventura: int
    numero: int
    fecha: str

class SesionUpdate(Sesion):
    id_aventura: int | None = None
    numero: int | None = None
    fecha: str | None = None