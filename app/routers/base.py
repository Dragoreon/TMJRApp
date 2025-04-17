from pydantic import BaseModel
from fastapi import HTTPException
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SUPABASE_SUPAFAST_URL')
key = os.getenv('SUPABASE_SUPAFAST_KEY')
supabase: Client = create_client(url, key)

def is_empty(model: BaseModel) -> bool:
    return model is None or model.data == []

def get(id: int, table_name: str) -> BaseModel:
    object = supabase.table(table_name).select('*').eq('id', id).execute()
    if is_empty(object): return None
    return object

def not_found():
    raise HTTPException(status_code=404, detail=f"No existe.")

def check_exists(id: int, table_name: str):
    if get(id, table_name) is None: not_found()