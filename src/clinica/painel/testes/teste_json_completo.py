import requests

# Teste da nova lógica com JSON completo para cada vaga
base_url = 'http://127.0.0.1:8001'

print("=== Teste da Nova Lógica: JSON Completo por Vaga ===")

# Simular dados do formulário
medico_id = 1

# Dados agrupados por vaga (como viria do formulário)
vagas_atualizadas = {
    '1': {
        'segunda': medico_id,  # Selecionado
        'terca': None,         # Vazio
        'quarta': medico_id,   # Selecionado
        'quinta': None,        # Vazio
        'sexta': None          # Vazio
    },
    '2': {
        'segunda': None,       # Vazio
        'terca': medico_id,    # Selecionado
        'quarta': None,        # Vazio
        'quinta': medico_id,   # Selecionado
        'sexta': None          # Vazio
    },
    '3': {
        'segunda': None,       # Vazio
        'terca': None,         # Vazio
        'quarta': medico_id,   # Selecionado
        'quinta': None,        # Vazio
        'sexta': None          # Vazio
    }
}

# Processar cada vaga com JSON completo
for vaga_id, dias_selecionados in vagas_atualizadas.items():
    try:
        # Buscar dados atuais da vaga
        vaga_response = requests.get(f'{base_url}/vagas/{vaga_id}/')
        vaga_response.raise_for_status()
        vaga_atual = vaga_response.json()
        
        # Criar JSON completo para atualização
        update_data = {
            "status": vaga_atual.get("status", ""),
            "segunda": dias_selecionados.get("segunda", vaga_atual.get("segunda")),
            "terca": dias_selecionados.get("terca", vaga_atual.get("terca")),
            "quarta": dias_selecionados.get("quarta", vaga_atual.get("quarta")),
            "quinta": dias_selecionados.get("quinta", vaga_atual.get("quinta")),
            "sexta": dias_selecionados.get("sexta", vaga_atual.get("sexta")),
            "max_pacientes": vaga_atual.get("max_pacientes", 0),
            "pacientes_atuais": vaga_atual.get("pacientes_atuais", 0)
        }
        
        # Atualizar a vaga via API com JSON completo
        update_response = requests.put(f'{base_url}/vagas/{vaga_id}/', json=update_data)
        update_response.raise_for_status()
        
        print(f"✅ Vaga {vaga_id} atualizada:")
        print(f"   JSON enviado: {update_data}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao atualizar vaga {vaga_id}: {e}")

print("\n=== Verificação Final ===")
# Verificar resultados
for vaga_id in ['1', '2', '3']:
    try:
        response = requests.get(f'{base_url}/vagas/{vaga_id}/')
        if response.status_code == 200:
            vaga = response.json()
            print(f"Vaga {vaga_id}: segunda={vaga['segunda']}, terca={vaga['terca']}, quarta={vaga['quarta']}, quinta={vaga['quinta']}, sexta={vaga['sexta']}")
    except Exception as e:
        print(f"❌ Erro ao verificar vaga {vaga_id}: {e}")
