import requests

# Simular envio do formulário como viria do frontend
base_url = 'http://127.0.0.1:8001'

# Dados que viriam do formulário POST
form_data = {
    'clinica': '1',
    'medico_id': '1',
    # Selectboxes das vagas (exemplo: 3 vagas × 5 dias = 15 campos)
    'vaga_1_segunda': '1',      # Selecionado - atribui médico 1
    'vaga_1_terca': '',         # Vazio - limpa campo
    'vaga_1_quarta': '1',      # Selecionado - atribui médico 1
    'vaga_1_quinta': '',       # Vazio - limpa campo
    'vaga_1_sexta': '',        # Vazio - limpa campo
    
    'vaga_2_segunda': '',      # Vazio - limpa campo
    'vaga_2_terca': '2',       # Selecionado - atribui médico 2
    'vaga_2_quarta': '',       # Vazio - limpa campo
    'vaga_2_quinta': '2',      # Selecionado - atribui médico 2
    'vaga_2_sexta': '',        # Vazio - limpa campo
    
    'vaga_3_segunda': '',      # Vazio - limpa campo
    'vaga_3_terca': '',        # Vazio - limpa campo
    'vaga_3_quarta': '1',      # Selecionado - atribui médico 1
    'vaga_3_quinta': '',       # Vazio - limpa campo
    'vaga_3_sexta': '',        # Vazio - limpa campo
}

print("=== Simulando processamento do formulário ===")

# Processar como na view do Django
medico_id = 1
for key, value in form_data.items():
    if key.startswith('vaga_'):
        # Extrair informações do selectbox
        parts = key.split('_')
        vaga_id = parts[1]
        dia = parts[2]
        
        # Determinar valor: ID do médico se selecionado, None se vazio
        medico_value = medico_id if value and value.strip() else None
        
        # Atualizar a vaga via API
        vaga_update_request = f'{base_url}/vagas/{vaga_id}/'
        update_data = {dia: medico_value}
        
        try:
            update_response = requests.put(vaga_update_request, json=update_data)
            update_response.raise_for_status()
            status = "✅" if medico_value else "🗑️"
            print(f"{status} Vaga {vaga_id} - {dia}: {medico_value}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao atualizar vaga {vaga_id}: {e}")

print("\n=== Verificação final ===")
# Verificar resultados
for vaga_id in ['1', '2', '3']:
    response = requests.get(f'{base_url}/vagas/{vaga_id}/')
    if response.status_code == 200:
        vaga = response.json()
        print(f"Vaga {vaga_id}: segunda={vaga['segunda']}, terca={vaga['terca']}, quarta={vaga['quarta']}, quinta={vaga['quinta']}, sexta={vaga['sexta']}")
