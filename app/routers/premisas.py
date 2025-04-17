from fastapi import HTTPException, APIRouter
from models.premisa import Premisa, PremisaUpdate
from .base import *

router = APIRouter()
table_name = 'Premisa'

@router.get("/premisa")
async def leer_premisas(limit: int = 10, offset: int = 0):
    premisa = supabase.table(table_name).select('*').limit(limit).offset(offset).execute()
    return premisa

@router.post("/premisa/create")
async def crear_premisa(premisa: Premisa):
    data = premisa.model_dump(exclude='id')
    try:
        response = supabase.table(table_name).insert(data).execute()
        return response
    except Exception as error:
        raise HTTPException (status_code=500, detail="Ocurrió un error")

@router.post("/premisa/update/{id}")
async def editar_premisa(id: int, premisa: PremisaUpdate):
    check_exists(id, table_name)
    try:
        supabase.table(table_name).update(premisa.model_dump(exclude_unset=True)).eq("id", id).execute()
    except Exception as error:
        raise HTTPException(status_code=500, detail="No se pudo actualizar")
    return f"{table_name} se ha actualizado"

@router.delete("/premisa/delete/{id}")
async def borrar_premisa(id: int):
    check_exists(id, table_name)
    try:
        supabase.table(table_name).delete().eq("id", id).execute()
    except Exception as error:
        raise HTTPException(status_code=500, detail="No se pudo borrar")
    return f"{table_name} se ha borrado"

@router.get("/premisa/{id}")
async def leer_premisa(id: int):
    premisa = get(id, table_name)
    if is_empty(premisa): not_found()
    return Premisa(**premisa.data[0])