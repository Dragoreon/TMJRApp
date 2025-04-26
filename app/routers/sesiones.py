from fastapi import HTTPException, APIRouter
from models.sesion import Sesion, SesionUpdate
from schemas.tables import TableName as Table
from .base import *
from datetime import datetime, timedelta

router = APIRouter()
main_table = Table.SESION.value
detail_query = f'id, numero, fecha, {Table.AVENTURA.value}!inner(id, lugar, abierta_inscripcion, {Table.PREMISA.value}!inner(titulo, sistema, id_master, descripcion, aviso_contenido))'

def check_limits(limit: int, offset: int):
    if limit > 100:
        raise HTTPException(status_code=400, detail="El límite no puede ser mayor a 100")
    if offset < 0:
        raise HTTPException(status_code=400, detail="El offset no puede ser menor a 0")

@router.get("/sesion")
async def leer_sesiones(limit: int = 10, offset: int = 0, details: bool = False, soon: bool = False):
    check_limits(limit, offset)
    query = detail_query if details else '*'
    sesiones = None
    if soon:
        sesiones = supabase.table(main_table).select(query).gte("fecha", datetime.now().isoformat()).limit(limit).offset(offset).execute()
    else:
        sesiones = supabase.table(main_table).select(query).limit(limit).offset(offset).execute()
    return sesiones

@router.get("/sesion/this-week")
async def leer_sesiones(limit: int = 10, offset: int = 0, details: bool = False):
    check_limits(limit, offset)
    query = detail_query if details else '*'
    today = datetime.now()
    next_week = today + timedelta(days=7)
    sesiones = supabase.table(main_table).select(query).gte("fecha", today.isoformat()).lte("fecha", next_week.isoformat()).limit(limit).offset(offset).execute()
    return sesiones

@router.post("/sesion/create")
async def crear_sesion(sesion: Sesion):
    data = sesion.model_dump(exclude='id')
    try:
        response = supabase.table(main_table).insert(data).execute()
        return response
    except Exception as error:
        raise HTTPException (status_code=500, detail="Ocurrió un error")

@router.post("/sesion/update/{id}")
async def editar_sesion(id: int, sesion: SesionUpdate):
    check_exists(id)
    try:
        supabase.table(main_table).update(sesion.model_dump(exclude_unset=True)).eq("id", id).execute()
    except Exception as error:
        raise HTTPException(status_code=500, detail="No se pudo actualizar")
    return f"{main_table} se ha actualizado"

@router.delete("/sesion/delete/{id}")
async def borrar_sesion(id: int):
    check_exists(id)
    try:
        supabase.table(main_table).delete().eq("id", id).execute()
    except Exception as error:
        raise HTTPException(status_code=500, detail="No se pudo borrar")
    return f"{main_table} se ha borrado"

@router.get("/sesion/{id}")
async def leer_sesion(id: int):
    sesion = get(id, main_table)
    if is_empty(sesion): not_found()
    return Sesion(**sesion.data[0])