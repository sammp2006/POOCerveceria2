 
from datetime import datetime
import re

def fecha_valida(fecha: str) -> bool:
    """
    Funcion que verifica si la fecha ingresada como argumento es válida en el formato DD/MM/AAAA.
    Retorna True si la fecha es válida, False en caso contrario.
    """
    try:
        datetime.strptime(fecha, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def es_alfa_numerico(cadena: str) -> bool:
    """
    Verifica si un string contiene solo letras y números.
    Retorna True si contiene solo letras y números, False en caso contrario.
    """
    return bool(re.fullmatch(r"[a-zA-Z0-9]+", cadena))

def formato_peso_volumen(cadena: str) -> bool:
    """
    Verifica si un string tiene el formato "<numero> ml" o "<numero> g".
    Retorna True si tiene el formato correcto, False en caso contrario.
    """
    return bool(re.fullmatch(r"\d+ (ml|g)", cadena))

def es_entero_no_negativo(cadena: str) -> bool:
    """
    Verifica si un string representa un número entero no negativo.
    Retorna True si es un número entero no negativo, False en caso contrario.
    """
    if isinstance(cadena, int):
        return True

    return bool(re.fullmatch(r"\d+", cadena))

def es_correo(cadena: str) -> bool:
    """
    Verifica si un string tiene el formato de una dirección de correo electrónico válida.
    Retorna True si es un correo válido, False en caso contrario.
    """
    return bool(re.fullmatch(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", cadena))