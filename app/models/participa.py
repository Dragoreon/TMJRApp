from pydantic import BaseModel

class Participa(BaseModel):
    id: int
    id_aventura: int
    id_usuaria: int
    id_rol: int

class ParticipaUpdate(Participa):
    id_aventura: int | None = None
    id_usuaria: int | None = None
    id_rol: int | None = None