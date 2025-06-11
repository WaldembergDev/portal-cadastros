import requests
from django.conf import settings
import os

def obter_distancia(cep_origem):
    api_url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    params = {
        "origins": cep_origem,
        "destinations": "21031790",
        "mode": "transit",
        "language": "pt-BR",
        "key": settings.MAPS_API_KEY
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status() 

        data = response.json()
        if data.get('rows')[0].get('elements')[0].get('status') == 'NOT_FOUND':
            return []
        dados_distancia = data.get('rows')[0].get('elements')[0].get('distance').get('value')
        dados_tempo = data.get('rows')[0].get('elements')[0].get('duration').get('text')
        dados = {'dados_distancia': dados_distancia,
                 'dados_tempo': dados_tempo}
        return dados

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return []
