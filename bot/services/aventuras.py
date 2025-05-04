from config.settings import logger, API_BASE_URL
import requests
from requests.models import Response


# Métodos crud para aventuras
def process_response(response: Response, error_message="Error en la solicitud"):
    """Procesa la respuesta de la API."""
    if response.ok:
        return response.json()["data"]
    else:
        logger.error(f"Error in response: {response}")
        raise Exception(f"{error_message}: {response.status_code}")


def get_aventuras():
    """Obtiene la lista de aventuras"""
    url = f"{API_BASE_URL}/aventura"
    response = requests.get(url)
    logger.info(f"Response obj: {response}")
    return process_response(response, "Error al obtener aventuras")


def get_aventura(id: int):
    """Obtiene una aventura dado su id."""
    logger.info(f"Get aventura with id: {id}")
    url = f"{API_BASE_URL}/aventura/{id}"
    response = requests.get(url)
    logger.info(f"Response obj: {response}")
    return process_response(response, "Error al obtener la aventura")
