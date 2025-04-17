from fastapi import HTTPException, APIRouter
from models.participa import Participa, ParticipaUpdate
from .base import *

router = APIRouter()
table_name = 'Participa'

@router.get("/participa")
async def leer_participas(limit: int = 10, offset: int = 0):
    participa = supabase.table(table_name).select('*').limit(limit).offset(offset).execute()
    return participa

@router.post("/participa/create")
async def crear_participa(participa: Participa):
    data = participa.model_dump(exclude='id')
    try:
        response = supabase.table(table_name).insert(data).execute()
        return response
    except Exception as error:
        raise HTTPException (status_code=500, detail="Ocurrió un error")

@router.post("/participa/update/{id}")
async def editar_participa(id: int, participa: ParticipaUpdate):
    check_exists(id)
    try:
        supabase.table(table_name).update(participa.model_dump(exclude_unset=True)).eq("id", id).execute()
    except Exception as error:
        raise HTTPException(status_code=500, detail="No se pudo actualizar")
    return f"{table_name} se ha actualizado"

@router.delete("/participa/delete/{id}")
async def borrar_participa(id: int):
    check_exists(id)
    try:
        supabase.table(table_name).delete().eq("id", id).execute()
    except Exception as error:
        raise HTTPException(status_code=500, detail="No se pudo borrar")
    return f"{table_name} se ha borrado"

@router.get("/participa/{id}")
async def leer_participa(id: int):
    participa = get(id, table_name)
    if is_empty(participa): not_found()
    return Participa(**participa.data[0])