import logging
import requests
from requests.models import Response
import os
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv('API_BASE_URL')

logger = logging.getLogger(__name__)

def api_request(method: str, endpoint: str, data=None):
    """Realiza una solicitud a la API y maneja la respuesta."""
    url = f"{API_BASE_URL}/{endpoint}"
    response = requests.request(method, url, json=data)
    logging.info(f"Response obj: {response}")
    if response.ok:
        return response.json()['data']
    else:
        raise Exception(f"Error en la solicitud: {response.status_code}")

# Métodos crud para partidas
def get_partidas(details: bool = False, soon: bool = False):
    endpoint = f"sesion?details={details}&soon={soon}"
    return api_request("GET", endpoint)

def get_partidas_week(details: bool = False):
    """Lista de partidas de la semana."""
    endpoint = f"sesion/this-week?details={details}"
    return api_request("GET", endpoint)

def get_partida(id:int, details: bool = False):
    endpoint = f"sesion/{id}?details={details}"
    return api_request("GET", endpoint)
    