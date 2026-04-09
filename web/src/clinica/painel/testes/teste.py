import requests

base_url = 'http://127.0.0.1:8001'
clinica_id = 1

id = 2
response = requests.get(f'http://localhost:8001/medico-sala/optimized/{id}?clinica_id={clinica_id}')

if response.status_code == 200:
    vagas= response.json()['vagas']
    medicos = response.json()['medico']
    
    vaga = vagas[0]
else:
    vagas = response.status_code
    medicos = response.status_code
    
print(medicos)
print(vagas)
print(vaga)