from enum import Enum

# Define the table names 
class TableName(str, Enum):
    USUARIA = "Usuaria"
    SESION = "Sesion"
    AVENTURA = "Aventura"
    ROL = "Rol"
    PARTIDA = "Partida"
    PARTICIPA = "Participa"
    ESPERA = "Lista_espera"
    PREMISA = "Premisa"