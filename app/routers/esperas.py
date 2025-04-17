from fastapi import HTTPException, APIRouter
from models.espera import Espera, EsperaUpdate
from .base import *

router = APIRouter()
table_name = 'Espera'

@router.get("/espera")
async def leer_esperas(limit: int = 10, offset: int = 0):
    espera = supabase.table(table_name).select('*').limit(limit).offset(offset).execute()
    return espera

@router.post("/espera/create")
async def crear_espera(espera: Espera):
    data = espera.model_dump(exclude='id')
    try:
        response = supabase.table(table_name).insert(data).execute()
        return response
    except Exception as error:
        raise HTTPException (status_code=500, detail="Ocurrió un error")

@router.post("/espera/update/{id}")
async def editar_espera(id: int, espera: EsperaUpdate):
    check_exists(id)
    try:
        supabase.table(table_name).update(espera.model_dump(exclude_unset=True)).eq("id", id).execute()
    except Exception as error:
        raise HTTPException(status_code=500, detail="No se pudo actualizar")
    return f"{table_name} se ha actualizado"

@router.delete("/espera/delete/{id}")
async def borrar_espera(id: int):
    check_exists(id)
    try:
        supabase.table(table_name).delete().eq("id", id).execute()
    except Exception as error:
        raise HTTPException(status_code=500, detail="No se pudo borrar")
    return f"{table_name} se ha borrado"

@router.get("/espera/{id}")
async def leer_espera(id: int):
    espera = get(id, table_name)
    if is_empty(espera): not_found()
    return Espera(**espera.data[0])