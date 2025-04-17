from fastapi import HTTPException, APIRouter
from models.rol import Rol, RolUpdate
from .base import *

router = APIRouter()
table_name = 'Rol'

@router.get("/rol")
async def leer_roles(limit: int = 10, offset: int = 0):
    rol = supabase.table(table_name).select('*').limit(limit).offset(offset).execute()
    return rol

@router.post("/rol/create")
async def crear_rol(rol: Rol):
    data = rol.model_dump(exclude='id')
    try:
        response = supabase.table(table_name).insert(data).execute()
        return response
    except Exception as error:  
        raise HTTPException (status_code=500, detail="Ocurrió un error")

@router.post("/rol/update/{id}")
async def editar_rol(id: int, rol: RolUpdate):
    check_exists(id)
    try:
        supabase.table(table_name).update(rol.model_dump(exclude_unset=True)).eq("id", id).execute()
    except Exception as error:
        raise HTTPException(status_code=500, detail="No se pudo actualizar")
    return f"{table_name} se ha actualizado"

@router.delete("/rol/delete/{id}")
async def borrar_rol(id: int):
    check_exists(id)
    try:
        supabase.table(table_name).delete().eq("id", id).execute()
    except Exception as error:
        raise HTTPException(status_code=500, detail="No se pudo borrar")
    return f"{table_name} se ha borrado"

@router.get("/rol/{id}")
async def leer_rol(id: int):
    rol = get(id, table_name)
    if is_empty(rol): not_found()
    return Rol(**rol.data[0])