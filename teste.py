import requests
from pprint import pprint

cnpj = '03248364000183'
url = f'https://brasilapi.com.br/api/cnpj/v1/{cnpj}'

result = requests.get(url)

pprint(result.json())
