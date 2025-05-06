from enum import Enum, auto, unique


@unique
class States(Enum):
    MAIN_MENU = auto()
    PARTIDA_LISTA = auto()
    PARTIDA_DETALLES = auto()
    PARTIDA_UNIRSE = auto()
    PARTIDA_CREAR = auto()
    PARTIDA_CREAR_TITULO = auto()
    PARTIDA_CREAR_SISTEMA = auto()
