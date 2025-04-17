from fastapi import HTTPException, APIRouter
from models.sesion import Sesion, SesionUpdate
from .base import *

router = APIRouter()
table_name = 'Sesion'

@router.get("/sesion")
async def leer_sesiones(limit: int = 10, offset: int = 0):
    sesion = supabase.table(table_name).select('*').limit(limit).offset(offset).execute()
    return sesion

@router.post("/sesion/create")
async def crear_sesion(sesion: Sesion):
    data = sesion.model_dump(exclude='id')
    try:
        response = supabase.table(table_name).insert(data).execute()
        return response
    except Exception as error:
        raise HTTPException (status_code=500, detail="Ocurrió un error")

@router.post("/sesion/update/{id}")
async def editar_sesion(id: int, sesion: SesionUpdate):
    check_exists(id)
    try:
        supabase.table(table_name).update(sesion.model_dump(exclude_unset=True)).eq("id", id).execute()
    except Exception as error:
        raise HTTPException(status_code=500, detail="No se pudo actualizar")
    return f"{table_name} se ha actualizado"

@router.delete("/sesion/delete/{id}")
async def borrar_sesion(id: int):
    check_exists(id)
    try:
        supabase.table(table_name).delete().eq("id", id).execute()
    except Exception as error:
        raise HTTPException(status_code=500, detail="No se pudo borrar")
    return f"{table_name} se ha borrado"

@router.get("/sesion/{id}")
async def leer_sesion(id: int):
    sesion = get(id, table_name)
    if is_empty(sesion): not_found()
    return Sesion(**sesion.data[0])