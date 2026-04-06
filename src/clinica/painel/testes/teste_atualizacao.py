import requests

# Teste para atualizar uma vaga específica
base_url = 'http://127.0.0.1:8001'

# Dados de teste
vaga_id = 1
medico_id = 1
dia = 'segunda'

# Primeiro: atribuir médico
print("=== Teste 1: Atribuir médico ===")
response = requests.put(f'{base_url}/vagas/{vaga_id}/', json={dia: medico_id})
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

# Segundo: limpar (enviar None)
print("\n=== Teste 2: Limpar médico (enviar None) ===")
response = requests.put(f'{base_url}/vagas/{vaga_id}/', json={dia: None})
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

# Verificar resultado final
if response.status_code == 200:
    resultado = response.json()
    if resultado[dia] is None:
        print("✅ Campo limpo com sucesso!")
    else:
        print(f"❌ Campo não foi limpo. Valor atual: {resultado[dia]}")
else:
    print("❌ Erro ao limpar vaga")
