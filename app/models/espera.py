from pydantic import BaseModel

class Espera(BaseModel):
    id: int
    inicio: str
    id_aventura: int
    id_usuaria: int

class EsperaUpdate(Espera):
    id: int | None = None
    inicio: str | None = None
    id_usuaria: int | None = None