
from ..Wolfram_Alpha import *

def resolver_probabilidad_wolfram_alpha(mensaje):
    """
    Resuelve un problema de probabilidad usando Wolfram Alpha API.
    
    mensaje: str - Consulta en formato natural o estructurado.
    """
    # Realizar la consulta a Wolfram Alpha
    resultado = wolfram_alpha_query(mensaje)
    
    if 'error' in resultado:
        return resultado
    
    # Procesar el resultado para obtener información relevante
    pods = resultado.get('queryresult', {}).get('pods', [])
    
    # Extraer resultados relevantes
    resultados = {}
    for pod in pods:
        title = pod.get('title', '')
        subpods = pod.get('subpods', [])
        for subpod in subpods:
            plaintext = subpod.get('plaintext', '')
            if plaintext:
                resultados[title] = plaintext
    
    return {
        "success": True,
        "mensaje": "Consulta realizada a Wolfram Alpha",
        "consulta": mensaje,
        "resultados": resultados
    }