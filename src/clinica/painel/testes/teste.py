import requests

base_url = 'http://127.0.0.1:8001'

response = requests.get(f'{base_url}/vagas/clinica/1')

if response.status_code == 200:
    vagas= response.json()
else:
    vagas = response.status_code
    
    

print(vagas)