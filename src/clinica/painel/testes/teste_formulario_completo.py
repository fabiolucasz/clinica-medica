import requests

# Simular envio completo do formulário como viria do frontend
base_url = 'http://127.0.0.1:8001'

print("=== Simulação Completa do Formulário Frontend ===")

# Dados exatos que viriam do formulário HTML
form_data = {
    'clinica': '1',
    'medico_id': '1',
    'csrfmiddlewaretoken': 'demo-token',
    
    # Selectboxes das vagas (3 vagas × 5 dias = 15 campos)
    'vaga_1_segunda': '1',      # Selecionado
    'vaga_1_terca': '',         # Vazio - None
    'vaga_1_quarta': '1',      # Selecionado
    'vaga_1_quinta': '',       # Vazio - None
    'vaga_1_sexta': '',        # Vazio - None
    
    'vaga_2_segunda': '',      # Vazio - None
    'vaga_2_terca': '1',       # Selecionado
    'vaga_2_quarta': '',       # Vazio - None
    'vaga_2_quinta': '1',      # Selecionado
    'vaga_2_sexta': '',        # Vazio - None
    
    'vaga_3_segunda': '',      # Vazio - None
    'vaga_3_terca': '',        # Vazio - None
    'vaga_3_quarta': '1',      # Selecionado
    'vaga_3_quinta': '',       # Vazio - None
    'vaga_3_sexta': '',        # Vazio - None
}

# Lógica exata da view Django
medico_id = 1
vagas_atualizadas = {}

# 1. Agrupar dados por vaga_id
print("1. Agrupando dados por vaga_id...")
for key, value in form_data.items():
    if key.startswith('vaga_'):
        parts = key.split('_')
        vaga_id = parts[1]
        dia = parts[2]
        
        if vaga_id not in vagas_atualizadas:
            vagas_atualizadas[vaga_id] = {}
        
        # Atribuir médico ou None conforme seleção
        vagas_atualizadas[vaga_id][dia] = medico_id if value and value.strip() else None
        
        status = "✅" if value and value.strip() else "🗑️"
        print(f"   {status} vaga_{vaga_id}_{dia}: {vagas_atualizadas[vaga_id][dia]}")

# 2. Para cada vaga, buscar dados atuais e criar JSON completo
print("\n2. Criando JSON completo para cada vaga...")
for vaga_id, dias_selecionados in vagas_atualizadas.items():
    try:
        # Buscar dados atuais da vaga
        vaga_response = requests.get(f'{base_url}/vagas/{vaga_id}/')
        vaga_response.raise_for_status()
        vaga_atual = vaga_response.json()
        
        # Criar JSON completo para atualização (schema exato da API)
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
        vaga_update_request = f'{base_url}/vagas/{vaga_id}/'
        update_response = requests.put(vaga_update_request, json=update_data)
        update_response.raise_for_status()
        
        print(f"   ✅ Vaga {vaga_id} atualizada com JSON completo")
        print(f"      PUT /vagas/{vaga_id}/")
        print(f"      Body: {update_data}")
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erro ao atualizar vaga {vaga_id}: {e}")

print("\n3. Verificação Final ===")
# Verificar resultados
for vaga_id in ['1', '2', '3']:
    try:
        response = requests.get(f'{base_url}/vagas/{vaga_id}/')
        if response.status_code == 200:
            vaga = response.json()
            print(f"Vaga {vaga_id}: segunda={vaga['segunda']}, terca={vaga['terca']}, quarta={vaga['quarta']}, quinta={vaga['quinta']}, sexta={vaga['sexta']}")
    except Exception as e:
        print(f"❌ Erro ao verificar vaga {vaga_id}: {e}")

print("\n✅ Sistema funcionando com JSON completo dinâmico!")
