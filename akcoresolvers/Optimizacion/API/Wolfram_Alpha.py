import os
import requests

# Obtener la clave de API de Wolfram Alpha desde settings.py
WOLFRAM_ALPHA_APP_ID = os.getenv('WOLFRAM_ALPHA_APP_ID', '7RVT9W-Y8YXKKU353')

# URL base de Wolfram Alpha API (usaremos el endpoint 'v2/query' para más detalles)
WOLFRAM_ALPHA_API_URL = 'https://api.wolframalpha.com/v2/query' 

def wolfram_alpha_query(query):
    """
    Realiza una consulta a Wolfram Alpha API y devuelve el resultado en formato JSON.
    
    query: str - Consulta en formato natural o estructurado.
    """
    params = {
        'input': query,
        'appid': WOLFRAM_ALPHA_APP_ID,
        'format': 'plaintext', 
        'output': 'json'
    }
    
    try:
        response = requests.get(WOLFRAM_ALPHA_API_URL, params=params)
        response.raise_for_status()  # Lanza una excepción si la respuesta no es exitosa
        
        return response.json()  # Devuelve el resultado en formato JSON
    except requests.exceptions.RequestException as e:
        return {"error": f"Error al realizar la consulta a Wolfram Alpha: {str(e)}"}