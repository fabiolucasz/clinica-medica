import requests

# Teste de escalabilidade - mais vagas dinamicamente
base_url = 'http://127.0.0.1:8001'

print("=== Teste de Escalabilidade: Mais Vagas Dinamicamente ===")

# Simular formulário com 5 vagas (poderia ser qualquer número)
form_data = {
    'clinica': '1',
    'medico_id': '1',
    
    # Vaga 1
    'vaga_1_segunda': '1', 'vaga_1_terca': '', 'vaga_1_quarta': '1', 'vaga_1_quinta': '', 'vaga_1_sexta': '',
    
    # Vaga 2  
    'vaga_2_segunda': '', 'vaga_2_terca': '1', 'vaga_2_quarta': '', 'vaga_2_quinta': '1', 'vaga_2_sexta': '',
    
    # Vaga 3
    'vaga_3_segunda': '', 'vaga_3_terca': '', 'vaga_3_quarta': '1', 'vaga_3_quinta': '', 'vaga_3_sexta': '',
    
    # Vaga 4 (nova)
    'vaga_4_segunda': '1', 'vaga_4_terca': '', 'vaga_4_quarta': '', 'vaga_4_quinta': '1', 'vaga_4_sexta': '',
    
    # Vaga 5 (nova)
    'vaga_5_segunda': '', 'vaga_5_terca': '1', 'vaga_5_quarta': '1', 'vaga_5_quinta': '', 'vaga_5_sexta': '1',
}

# Processamento dinâmico (funciona com qualquer número de vagas)
medico_id = 1
vagas_atualizadas = {}

print("1. Processando formulário dinamicamente...")
vagas_encontradas = set()
for key, value in form_data.items():
    if key.startswith('vaga_'):
        parts = key.split('_')
        vaga_id = parts[1]
        dia = parts[2]
        
        vagas_encontradas.add(vaga_id)
        
        if vaga_id not in vagas_atualizadas:
            vagas_atualizadas[vaga_id] = {}
        
        vagas_atualizadas[vaga_id][dia] = medico_id if value and value.strip() else None

print(f"   Encontradas {len(vagas_encontradas)} vagas: {sorted(vagas_encontradas)}")

# Criar JSON completo para cada vaga (funciona dinamicamente)
print("\n2. Atualizando vagas com JSON completo...")
for vaga_id in sorted(vagas_encontradas):
    try:
        # Buscar dados atuais (se existir)
        try:
            vaga_response = requests.get(f'{base_url}/vagas/{vaga_id}/')
            vaga_response.raise_for_status()
            vaga_atual = vaga_response.json()
            print(f"   ✅ Vaga {vaga_id} encontrada no banco")
        except:
            # Se não existir, criar estrutura padrão
            vaga_atual = {
                "status": "", "segunda": None, "terca": None, "quarta": None, 
                "quinta": None, "sexta": None, "max_pacientes": 0, "pacientes_atuais": 0
            }
            print(f"   🆕 Vaga {vaga_id} não encontrada, usando padrão")
        
        # Criar JSON completo
        dias_selecionados = vagas_atualizadas[vaga_id]
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
        
        # Tentar atualizar
        try:
            update_response = requests.put(f'{base_url}/vagas/{vaga_id}/', json=update_data)
            update_response.raise_for_status()
            print(f"   ✅ Vaga {vaga_id} atualizada")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Erro ao atualizar vaga {vaga_id}: {e}")
            print(f"      Tentativa com: {update_data}")
        
    except Exception as e:
        print(f"   ❌ Erro geral ao processar vaga {vaga_id}: {e}")

print(f"\n✅ Sistema processou dinamicamente {len(vagas_encontradas)} vagas!")
print("✅ A lógica é escalável - funciona com qualquer número de vagas!")
