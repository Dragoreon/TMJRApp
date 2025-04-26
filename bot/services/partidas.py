import logging
import requests
from requests.models import Response
import os
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv('API_BASE_URL')

logger = logging.getLogger(__name__)

# Métodos crud para partidas
def process_response(response : Response, error_message="Error en la solicitud"):
    """Procesa la respuesta de la API."""
    if response.ok:
        return response.json()['data']
    else:
        raise Exception(f"{error_message}: {response.status_code}")

def get_partidas(details: bool = False, soon: bool = False):
    """Obtiene la lista de partidas con todos los detalles de la aventura."""
    url = f"{API_BASE_URL}/sesion?details={details}&soon={soon}"
    response = requests.get(url)
    logging.info(f"Response obj: {response}")
    return process_response(response, "Error al obtener partidas")

def get_partidas_week(details: bool = False):
    """Lista de partidas de la semana."""
    url = f"{API_BASE_URL}/sesion/this-week?details={details}"
    response = requests.get(url)
    logging.info(f"Response obj: {response}")
    return process_response(response, "Error al obtener partidas")

