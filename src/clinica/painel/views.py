from datetime import datetime
import json
from struct import pack
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
import requests
import json
import concurrent.futures
from datetime import datetime
from django.db.models import Q
from .models import Paciente, Medico, Tipo_conselho, Estados, Clinicas, Especialidades, Salas, Vagas, Agendamentos
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.utils import timezone
import webbrowser
import requests
from mysite.views import token_required

base_url = 'http://127.0.0.1:8001'

# Views dos Pacientes

def cadastrar_paciente(request):
    """
    Cadastra um novo paciente
    """
    url_estados = f'{base_url}/estados/'
    estados = requests.get(url_estados).json()

    # TODO: Implementar a verificação de CPF válido e preenchimento automático do campo de CEP, Mensagem de erro caso o CPF seja inválido ou já cadastrado.

    if request.method == 'POST':
        # Processar o formulário
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        celular = request.POST.get('celular')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        sexo = request.POST.get('sexo')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        estado_uf = request.POST.get('estado')
        foto_perfil = request.POST.get('foto')
        try:
            response = requests.post(
                f'{base_url}/pacientes/',
                json={
                    'nome': nome,
                    'password': senha,
                    'celular': celular,
                    'email': email,
                    'cpf': cpf,
                    'data_nascimento': data_nascimento,
                    'sexo': sexo,
                    'cep': cep,
                    'rua': rua,
                    'numero': numero,
                    'bairro': bairro,
                    'cidade': cidade,
                    'estado': estado_uf,
                    'role': "paciente",
                    'foto_perfil': foto_perfil
                })
            
            if response.status_code == 200:
                return redirect('painel:listar_pacientes')
            else:
                print(f"Erro na API - Status: {response.status_code}")
                print(f"Resposta: {response.text}")
        except Exception as e:
            print(f"Erro ao cadastrar paciente: {e}")
            return redirect('painel:listar_pacientes')
        
        # Enviar mensagem de boas-vindas
        mensagem = f"Seja bem-vindo(a) a nossa clínica, {nome.upper()}! Estamos felizes em tê-lo(a) conosco."
        url = f'http://web.whatsapp.com/send?phone={celular}&text={mensagem}'       
        
        # Abrir URL no navegador padrão do usuário
        try:
            webbrowser.open(url, new=2)
        except Exception as e:
            print(f"Erro ao abrir navegador: {e}")
        
        # Redirecionar para a lista de pacientes
        return redirect('/painel/listar_pacientes/')
        
    return render(request, 'painel/cadastrar_paciente.html', {'estados': estados})


def listar_pacientes(request):
    # Obter token da sessão
    token = request.session.get('fastapi_token')
    if not token:
        return redirect('/login/')
    
    # Headers com autenticação
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        url_pacientes = f'{base_url}/pacientes/'
        url_estados = f'{base_url}/estados/'
        
        # Requisições com autenticação
        pacientes_response = requests.get(url_pacientes, headers=headers)
        estados_response = requests.get(url_estados, headers=headers)
        
        if pacientes_response.status_code == 200:
            pacientes = pacientes_response.json()
        else:
            pacientes = []
            
        if estados_response.status_code == 200:
            estados = estados_response.json()
        else:
            estados = []
            
    except Exception as e:
        pacientes = []
        estados = []
        print(f"Erro ao buscar dados da API: {e}")
    
    return render(request, 'painel/listar_pacientes.html', {'pacientes': pacientes, 'estados': estados})

@token_required
def editar_paciente(request, id):
    # Obter token da sessão
    token = request.session.get('fastapi_token')
    if not token:
        return redirect('/login/')
    
    headers = {'Authorization': f'Bearer {token}'}
    url_paciente_id = f'{base_url}/pacientes/{id}/'
    
    try:
        paciente_response = requests.get(url_paciente_id, headers=headers)
        if paciente_response.status_code == 200:
            paciente = paciente_response.json()
        else:
            paciente = {}
    except Exception as e:
        paciente = {}
        print(f"Erro ao buscar paciente: {e}")
    
    if request.method == 'POST':
        # Processar o formulário
        nome = request.POST.get('nome')
        celular = request.POST.get('celular')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        sexo = request.POST.get('sexo')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        estado_id = request.POST.get('estado')
        foto_perfil = request.POST.get('foto', 'string')
        
        try:
            response = requests.put(url_paciente_id, json={
                'nome': nome,
                'email': email,
                'celular': celular,
                'cpf': cpf,
                'data_nascimento': data_nascimento,
                'sexo': sexo,
                'cep': cep,
                'rua': rua,
                'numero': numero,
                'bairro': bairro,
                'cidade': cidade,
                'estado': int(estado_id) if estado_id else 0,
                'role': "paciente",
                'foto_perfil': foto_perfil
            }, headers=headers)
            

            
            if response.status_code == 200:
                return redirect('painel:listar_pacientes')
        except Exception as e:
            print(f"Erro ao editar paciente: {e}")
    
    return render(request, 'painel/editar_paciente.html', {'paciente': paciente})


def excluir_paciente(request, id):
    url_paciente_id = f'{base_url}/pacientes/{id}/'
    response = requests.delete(url_paciente_id)
    if response.status_code == 200:
        return redirect('painel:listar_pacientes')
    return redirect('painel:listar_pacientes')


#Views dos Médicos
@token_required
def cadastrar_medico(request):

    url_conselho = f'{base_url}/tipo-conselho/'
    url_clinicas = f'{base_url}/clinicas/'
    url_estados = f'{base_url}/estados/'
    url_especialidades = f'{base_url}/especialidades/'
    url_medico = f'{base_url}/medicos'
    
    tipo_conselho = requests.get(url_conselho).json()
    clinicas = requests.get(url_clinicas).json()
    estados = requests.get(url_estados).json()
    especialidades = requests.get(url_especialidades).json()
    
    if request.method == 'POST':
        # Processar o formulário
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        celular = request.POST.get('celular')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        sexo = request.POST.get('sexo')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')
        foto_perfil = request.POST.get('foto_perfil')
        especialidade = request.POST.get('especialidade_id')
        tipo_conselho = request.POST.get('tipo_conselho_id')
        uf_conselho = request.POST.get('uf_conselho_id')
        numero_conselho = request.POST.get('numero_conselho')
        rqe = request.POST.get('rqe')
        valor_consulta = request.POST.get('valor_consulta')
        upload_documento = request.POST.get('upload_documento')
        senha = request.POST.get('senha')

        try:
            # === DEBUG: Exibir dados sendo enviados ===
            data_payload = {
                "nome": nome,
                "email": email,
                "celular": celular,
                "cpf": cpf,
                "data_nascimento": data_nascimento,
                "sexo": sexo,
                "cep": cep,
                "rua": rua,
                "numero": numero,
                "bairro": bairro,
                "cidade": cidade,
                "estado": estado,
                "role": "medico",
                "foto_perfil": foto_perfil,
                "especialidade": especialidade,
                "rqe": rqe,
                "valor_consulta": valor_consulta,
                "tipo_conselho": tipo_conselho,
                "uf_conselho": uf_conselho,
                "numero_conselho": numero_conselho,
                "upload_arquivo": upload_documento,
                "password": senha,
            }
            
            print("\n" + "="*50)
            print("DEBUG - Payload enviado para API:")
            print("="*50)
            for key, value in data_payload.items():
                print(f"{key}: {repr(value)} (tipo: {type(value).__name__})")
            print("="*50 + "\n")
            
            # Criar o medico
            response = requests.post(
                f'{base_url}/medicos',  
                json=data_payload)
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                medico = response.json()
                print(f"Médico retornado pela API: {medico}")
                print(f"ID do médico: {medico.get('id')}")
                # Redirecionar para a página de seleção de vagas com o ID do médico
                return redirect('painel:cadastrar_medico_sala', medico_id=medico.get('id'))
            else:
                # Erro da API - mostrar mensagem detalhada
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                if 'detail' in error_data:
                    error_message = f"Erro da API: {error_data['detail']}"
                else:
                    error_message = f"Erro ao cadastrar médico: Status {response.status_code} - {response.text}"
                
        except Exception as e:
            error_message = f"Erro ao cadastrar médico: {str(e)}"
            # Tratar erro de email duplicado
            if "UNIQUE constraint failed: painel_medico.email" in str(e):
                error_message = "Este e-mail já está cadastrado. Por favor, use outro e-mail."
            elif "UNIQUE constraint failed: painel_medico.cpf" in str(e):
                error_message = "Este CPF já está cadastrado. Por favor, verifique os dados."
            elif "UNIQUE constraint failed: painel_medico.celular" in str(e):
                error_message = "Este celular já está cadastrado. Por favor, use outro número."
            else:
                error_message = f"Erro ao cadastrar médico: {str(e)}"
            
            return render(request, 'painel/cadastrar_medico.html', {'tipo_conselho': tipo_conselho,'especialidades': especialidades, 'estados': estados, 'clinicas': clinicas})

    return render(request, 'painel/cadastrar_medico.html', {'tipo_conselho': tipo_conselho,'especialidades': especialidades, 'estados': estados, 'clinicas': clinicas})


def listar_medicos(request):
    token = request.session.get('fastapi_token')
    if not token:
        return redirect('/login/')
    headers = {'Authorization': f'Bearer {token}'}
    try:
        url_medicos = f'{base_url}/medicos'
        response = requests.get(url_medicos, headers=headers)
        
        if response.status_code == 200:
            medicos = response.json()
        else:
            medicos = []
    except Exception as e:
        medicos = []
        print(f"Erro ao listar médicos: {e}")
    return render(request, 'painel/medicos.html', {'medicos': medicos})


def cadastrar_medico_sala(request, medico_id):
    # Obter token da sessão
    token = request.session.get('fastapi_token')
    if not token:
        return redirect('/login/')
    
    # Headers com autenticação
    headers = {'Authorization': f'Bearer {token}'}
    
    # URLs da API local (rodando na mesma máquina)
    api_base_url = 'http://localhost:8001'
    
    # Otimização MÁXIMA: Endpoint otimizado com tudo pré-processado
    try:
        # Usar endpoint otimizado que já vem com nomes enriquecidos
        optimized_url = f'{api_base_url}/medico-sala/optimized/{medico_id}'
        response = requests.get(optimized_url, headers=headers)
        response.raise_for_status()
        
        dados_completos = response.json()
        
        medico = dados_completos['medico']
        vagas = dados_completos['vagas']  # Já vem com nomes enriquecidos!
        
        print(f"DEBUG: Carregamento OTIMIZADO - Médico ID {medico_id}")
        print(f"DEBUG: {len(vagas)} vagas pré-enriquecidas carregadas")
        print(f"DEBUG: Tempo de carregamento: MÍNIMO! (sem requisições adicionais)")
        
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição otimizada: {e}")
        return redirect('/login/')
    except Exception as e:
        print(f"Erro ao processar dados otimizados: {e}")
        return redirect('/login/')
    
    if request.method == 'POST':
        # Processar as vagas selecionadas usando a clínica padrão
        clinica_id = 1
        sala_id = request.POST.get('sala')
        
        # Pegar o medico_id do formulário (hidden field)
        medico_id_form = request.POST.get('medico_id')
        print(f"DEBUG: medico_id da URL: {medico_id}")
        print(f"DEBUG: medico_id do formulário: {medico_id_form}")
        
        # Usar o medico_id do formulário (prioridade) ou da URL
        medico_id_atual = medico_id_form if medico_id_form else medico_id
        print(f"DEBUG: medico_id final usado: {medico_id_atual}")
        
        # Processar todos os selectboxes - agrupar por vaga_id
        vagas_atualizadas = {}
        
        print(f"\nDEBUG: Processando formulário POST:")
        print(f"Médico atual ID: {medico_id_atual}")
        print(f"Dados recebidos:")
        for key, value in request.POST.items():
            if key.startswith('vaga_'):
                print(f"  {key}: {value}")
        
        # Primeiro, agrupar todos os dados por vaga_id
        for key, value in request.POST.items():
            if key.startswith('vaga_'):
                parts = key.split('_')
                vaga_id = parts[1]
                dia = parts[2]
                
                # Apenas processar se o valor não estiver vazio e for o ID do médico atual
                if value and value.strip() and value == str(medico_id_atual):
                    if vaga_id not in vagas_atualizadas:
                        vagas_atualizadas[vaga_id] = {}
                    
                    # Atribuir médico atual APENAS para os campos selecionados
                    vagas_atualizadas[vaga_id][dia] = medico_id_atual
        
        print(f"Vagas a serem atualizadas: {vagas_atualizadas}\n")
        
        # Otimização: Processar vagas em lote usando requisições concorrentes diretas
        if vagas_atualizadas:
            print(f"DEBUG: Processando {len(vagas_atualizadas)} vagas em paralelo")
            
            # Primeiro, buscar todas as vagas atuais para manter os médicos existentes
            def buscar_vaga_atual(vaga_id):
                try:
                    response = requests.get(f'{api_base_url}/vagas/{vaga_id}', headers=headers)
                    response.raise_for_status()
                    return vaga_id, response.json()
                except requests.exceptions.RequestException as e:
                    print(f"❌ Erro ao buscar vaga {vaga_id}: {e}")
                    return vaga_id, None
            
            # Buscar vagas em paralelo
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                future_to_vaga = {executor.submit(buscar_vaga_atual, vaga_id): vaga_id for vaga_id in vagas_atualizadas.keys()}
                
                vagas_atuais = {}
                for future in concurrent.futures.as_completed(future_to_vaga):
                    vaga_id = future_to_vaga[future]
                    try:
                        vaga_id_result, vaga_data = future.result()
                        if vaga_data:
                            vagas_atuais[vaga_id_result] = vaga_data
                    except Exception as e:
                        print(f"❌ Erro ao processar vaga {vaga_id}: {e}")
            
            # Agora atualizar mantendo os médicos existentes
            def atualizar_vaga_com_preservacao(vaga_id):
                try:
                    dias_selecionados = vagas_atualizadas[vaga_id]
                    vaga_atual = vagas_atuais.get(vaga_id)
                    
                    if not vaga_atual:
                        return vaga_id, False, "Vaga não encontrada"
                    
                    print(f"DEBUG: Vaga {vaga_id} - Estado ANTES da atualização:")
                    print(f"  Segunda: {vaga_atual.get('segunda')} -> será: {dias_selecionados.get('segunda') if 'segunda' in dias_selecionados else vaga_atual.get('segunda')}")
                    print(f"  Terça: {vaga_atual.get('terca')} -> será: {dias_selecionados.get('terca') if 'terca' in dias_selecionados else vaga_atual.get('terca')}")
                    print(f"  Quarta: {vaga_atual.get('quarta')} -> será: {dias_selecionados.get('quarta') if 'quarta' in dias_selecionados else vaga_atual.get('quarta')}")
                    print(f"  Quinta: {vaga_atual.get('quinta')} -> será: {dias_selecionados.get('quinta') if 'quinta' in dias_selecionados else vaga_atual.get('quinta')}")
                    print(f"  Sexta: {vaga_atual.get('sexta')} -> será: {dias_selecionados.get('sexta') if 'sexta' in dias_selecionados else vaga_atual.get('sexta')}")
                    
                    # Manter os médicos existentes e atualizar apenas os dias selecionados
                    update_data = {
                        "segunda": dias_selecionados.get("segunda") if "segunda" in dias_selecionados else vaga_atual.get("segunda"),
                        "terca": dias_selecionados.get("terca") if "terca" in dias_selecionados else vaga_atual.get("terca"),
                        "quarta": dias_selecionados.get("quarta") if "quarta" in dias_selecionados else vaga_atual.get("quarta"),
                        "quinta": dias_selecionados.get("quinta") if "quinta" in dias_selecionados else vaga_atual.get("quinta"),
                        "sexta": dias_selecionados.get("sexta") if "sexta" in dias_selecionados else vaga_atual.get("sexta"),
                    }
                    
                    # Remover apenas valores None (quando usuário deselecionou)
                    update_data = {k: v for k, v in update_data.items() if v is not None}
                    
                    print(f"DEBUG: Atualizando vaga {vaga_id} com dados: {update_data}")
                    
                    update_response = requests.put(f'{api_base_url}/vagas/{vaga_id}', json=update_data, headers=headers)
                    update_response.raise_for_status()
                    return vaga_id, True, "Sucesso"
                    
                except requests.exceptions.RequestException as e:
                    return vaga_id, False, str(e)
            
            # Processar todas as atualizações em paralelo
            with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
                future_to_vaga = {executor.submit(atualizar_vaga_com_preservacao, vaga_id): vaga_id for vaga_id in vagas_atualizadas.keys()}
                
                sucessos = 0
                falhas = 0
                for future in concurrent.futures.as_completed(future_to_vaga):
                    vaga_id = future_to_vaga[future]
                    try:
                        vaga_id_result, success, message = future.result()
                        if success:
                            print(f"✅ Vaga {vaga_id_result} atualizada com sucesso")
                            sucessos += 1
                        else:
                            print(f"❌ Erro ao atualizar vaga {vaga_id_result}: {message}")
                            falhas += 1
                    except Exception as e:
                        print(f"❌ Erro ao processar atualização da vaga {vaga_id}: {e}")
                        falhas += 1
                
                print(f"DEBUG: Processamento concluído - {sucessos} sucessos, {falhas} falhas")
        
        # Redirecionar sempre após processar o formulário
        return redirect('painel:listar_medicos')
    
    return render(request, 'painel/cadastrar_medico_sala.html', {
        'vagas': json.dumps(vagas),
        'medico': medico
    })
    
    # Debug final para garantir que o médico correto foi passado
    print(f"DEBUG FINAL - Médico passado para template: {medico}")
    print(f"DEBUG FINAL - Médico ID: {medico.get('id') if medico else 'N/A'}")
    print(f"DEBUG FINAL - Médico Nome: {medico.get('nome') if medico else 'N/A'}")


# Consultas e Agendamentos

def buscar_pacientes(request):
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse({'pacientes': []})
    
    pacientes = Paciente.objects.filter(
        nome__icontains=query
    ).values('id', 'nome', 'cpf', 'celular')[:10]
    
    return JsonResponse({'pacientes': list(pacientes)})


def agendar_consulta(request):
    medicos = Medico.objects.all()
    vagas = Vagas.objects.select_related('sala', 'clinica', 'segunda', 'terca', 'quarta', 'quinta', 'sexta').all()
    
    # Serializar vagas para JSON
    vagas_data = []
    for vaga in vagas:
        vaga_dict = {
            'clinica': vaga.clinica.nome,
            'sala': vaga.sala.nome,
            'turno': vaga.turno,
            'hora_inicio': str(vaga.hora_inicio),
            'hora_fim': str(vaga.hora_fim),
            'max_pacientes': vaga.max_pacientes,
            'pacientes_atuais': vaga.pacientes_atuais,
            'segunda': vaga.segunda.id if vaga.segunda else None,
            'terca': vaga.terca.id if vaga.terca else None,
            'quarta': vaga.quarta.id if vaga.quarta else None,
            'quinta': vaga.quinta.id if vaga.quinta else None,
            'sexta': vaga.sexta.id if vaga.sexta else None,
        }
        vagas_data.append(vaga_dict)
    
    if request.method == 'POST':
        # Processar o agendamento
        paciente_id = request.POST.get('paciente_id')
        medico_id = request.POST.get('medico')
        data = request.POST.get('data')
        turno = request.POST.get('turno')  # Agora é o turno
        
        # Validar campos obrigatórios
        if not all([paciente_id, medico_id, data, turno]):
            error_message = "Por favor, preencha todos os campos obrigatórios."
            return render(request, 'painel/agendar_consulta.html', {
                'medicos': medicos,
                'vagas_json': json.dumps(vagas_data),
                'error': error_message
            })
        
        # Buscar paciente
        paciente = get_object_or_404(Paciente, id=paciente_id)
        
        # Buscar médico
        medico = get_object_or_404(Medico, id=medico_id)
        
        # Encontrar a vaga correspondente
        data_obj = datetime.strptime(data, '%Y-%m-%d').date()
        dia_semana = data_obj.weekday()  # 0=Segunda, 6=Domingo
        nomes_dias = ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']
        nome_dia = nomes_dias[dia_semana]
        
        # Buscar vaga do médico no dia com base no turno
        vaga = None
        if nome_dia == 'segunda':
            vaga = Vagas.objects.filter(segunda=medico, turno=turno).first()
        elif nome_dia == 'terca':
            vaga = Vagas.objects.filter(terca=medico, turno=turno).first()
        elif nome_dia == 'quarta':
            vaga = Vagas.objects.filter(quarta=medico, turno=turno).first()
        elif nome_dia == 'quinta':
            vaga = Vagas.objects.filter(quinta=medico, turno=turno).first()
        elif nome_dia == 'sexta':
            vaga = Vagas.objects.filter(sexta=medico, turno=turno).first()
        
        if vaga and vaga.pacientes_atuais < vaga.max_pacientes:
            # Criar agendamento
            agendamento = Agendamentos.objects.create(
                clinica=vaga.clinica,
                sala=vaga.sala,
                paciente=paciente,
                medico=medico,
                data_consulta=data_obj,  # Adicionar data da consulta
                turno=vaga.turno,
                hora_inicio=vaga.hora_inicio,  # Adicionar hora de início
                hora_fim=vaga.hora_fim,      # Adicionar hora de fim
                status='agendado'
            )
            
            # Incrementar contador de pacientes
            vaga.pacientes_atuais += 1
            vaga.save()
            
            # Enviar mensagem de confirmação
            mensagem = f"Olá {paciente.nome}! Sua consulta com Dr(a). {medico.nome} foi agendada para {data} ({vaga.turno}) na clínica {vaga.clinica.nome}."
            url = f'http://web.whatsapp.com/send?phone={paciente.celular}&text={mensagem}'
            
            try:
                import webbrowser
                webbrowser.open(url, new=2)
            except Exception as e:
                print(f"Erro ao abrir navegador: {e}")
            
            return redirect('painel:listar_consultas')
        else:
            # Vaga não disponível
            error_message = "Desculpe, não há vagas disponíveis para este turno."
            return render(request, 'painel/agendar_consulta.html', {
                'medicos': medicos,
                'vagas_json': json.dumps(vagas_data),
                'error': error_message
            })
    
    return render(request, 'painel/agendar_consulta.html', {
        'medicos': medicos,
        'vagas_json': json.dumps(vagas_data)
    })


def listar_consultas(request):
    from datetime import date, timedelta, datetime
    clinicas = Clinicas.objects.all()
    clinica_selecionada = request.GET.get('clinica')
    medico_selecionado = request.GET.get('medico')
    
    # Obter parâmetros de data ou usar semana atual
    data_inicio_param = request.GET.get('data_inicio')
    data_fim_param = request.GET.get('data_fim')
    
    if data_inicio_param and data_fim_param:
        # Converter parâmetros para data
        try:
            data_inicio = datetime.strptime(data_inicio_param, '%d/%m').date()
            # Ajustar para o ano atual
            data_inicio = data_inicio.replace(year=date.today().year)
            data_fim = datetime.strptime(data_fim_param, '%d/%m').date()
            data_fim = data_fim.replace(year=date.today().year)
        except ValueError:
            # Se falhar, usar semana atual
            data_inicio = date.today()
            while data_inicio.weekday() != 0:  # Encontrar segunda-feira
                data_inicio -= timedelta(days=1)
            data_fim = data_inicio + timedelta(days=4)
    else:
        # Usar semana atual
        data_inicio = date.today()
        while data_inicio.weekday() != 0:  # Encontrar segunda-feira
            data_inicio -= timedelta(days=1)
        data_fim = data_inicio + timedelta(days=4)
    
    if clinica_selecionada:
        print(f"DEBUG: Clinica selecionada: {clinica_selecionada}")
        print(f"DEBUG: Data início: {data_inicio}, Data fim: {data_fim}")
        salas_da_clinica = Salas.objects.filter(clinica_id=clinica_selecionada)
        print(f"DEBUG: Salas encontradas: {salas_da_clinica.count()}")
        
        # Obter médicos que trabalham na clínica selecionada através das vagas
        from django.db.models import Q
        medicos_da_clinica = Medico.objects.filter(
            Q(segunda__sala__clinica_id=clinica_selecionada) |
            Q(terca__sala__clinica_id=clinica_selecionada) |
            Q(quarta__sala__clinica_id=clinica_selecionada) |
            Q(quinta__sala__clinica_id=clinica_selecionada) |
            Q(sexta__sala__clinica_id=clinica_selecionada)
        ).distinct()
        print(f"DEBUG: Médicos encontrados: {medicos_da_clinica.count()}")
        
        salas_data = []
        
        for sala in salas_da_clinica:
            agendamentos_sala = []
            
            for dia_offset in range(5):  # Segunda a Sexta
                data_dia = data_inicio + timedelta(days=dia_offset)
                data_str = data_dia.strftime('%Y-%m-%d')
                
                # Filtrar por médico se selecionado
                agendamentos_query = Agendamentos.objects.filter(
                    sala=sala,
                    data_consulta=data_dia
                )
                
                if medico_selecionado:
                    agendamentos_query = agendamentos_query.filter(medico_id=medico_selecionado)
                
                agendamentos_dia = agendamentos_query.select_related('paciente', 'medico').order_by('data_consulta')
                
                if agendamentos_dia:
                    print(f"DEBUG: Encontrados {agendamentos_dia.count()} agendamentos para sala {sala.nome} em {data_str}")
                
                for agendamento in agendamentos_dia:
                    especialidade = getattr(agendamento.medico, 'especialidade', None)
                    especialidade_nome = especialidade.nome if especialidade else 'Geral'
                    
                    agendamentos_sala.append({
                        'paciente': agendamento.paciente.nome,
                        'medico': agendamento.medico.nome,
                        'especialidade': especialidade_nome,
                        'hora_inicio': agendamento.hora_inicio.strftime('%H:%M') if agendamento.hora_inicio else '08:00',
                        'hora_fim': agendamento.hora_fim.strftime('%H:%M') if agendamento.hora_fim else '12:00',
                        'data_consulta': data_str,
                        'turno': agendamento.turno,
                        'total_pacientes': Agendamentos.objects.filter(
                            sala=sala, medico=agendamento.medico,
                            data_consulta=data_dia, turno=agendamento.turno
                        ).count()
                    })
            
            salas_data.append({
                'nome': sala.nome,
                'agendamentos_dia': agendamentos_sala
            })
        
        context = {
            'clinicas': clinicas,
            'clinica_selecionada': clinica_selecionada,
            'medicos': medicos_da_clinica,
            'medico_selecionado': medico_selecionado,
            'salas': salas_data,
            'datas_semana': {
                'segunda': (data_inicio).strftime('%Y-%m-%d'),
                'terca': (data_inicio + timedelta(days=1)).strftime('%Y-%m-%d'),
                'quarta': (data_inicio + timedelta(days=2)).strftime('%Y-%m-%d'),
                'quinta': (data_inicio + timedelta(days=3)).strftime('%Y-%m-%d'),
                'sexta': (data_inicio + timedelta(days=4)).strftime('%Y-%m-%d'),
            }
        }
    else:
        context = {
            'clinicas': clinicas,
            'clinica_selecionada': clinica_selecionada,
            'medicos': [],
            'medico_selecionado': medico_selecionado,
            'salas': [],
            'datas_semana': {
                'segunda': (data_inicio).strftime('%Y-%m-%d'),
                'terca': (data_inicio + timedelta(days=1)).strftime('%Y-%m-%d'),
                'quarta': (data_inicio + timedelta(days=2)).strftime('%Y-%m-%d'),
                'quinta': (data_inicio + timedelta(days=3)).strftime('%Y-%m-%d'),
                'sexta': (data_inicio + timedelta(days=4)).strftime('%Y-%m-%d'),
            }
        }
    
    return render(request, 'painel/listar_consultas.html', context)


def editar_consulta(request, id):
    return render(request, 'painel/editar_consulta.html')


def excluir_consulta(request, id):
    return render(request, 'painel/excluir_consulta.html')


# Configurações da clínica

## CRUD Clinica

def cadastrar_clinica(request):
    url_clinicas = f'{base_url}/clinicas/'
    url_estados = f'{base_url}/estados/'
    
    estados = requests.get(url_estados).json()
    
    if request.method == 'POST':
        # Processar o formulário
        nome = request.POST.get('nome')
        celular = request.POST.get('celular')
        celular2 = request.POST.get('celular2')
        email = request.POST.get('email')
        cnpj = request.POST.get('cnpj')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')

        try:
            response = requests.post(url_clinicas, json={
                'nome': nome,
                'celular': celular,
                'celular2': celular2,
                'email': email,
                'cnpj': cnpj,
                'cep': cep,
                'rua': rua,
                'numero': numero,
                'bairro': bairro,
                'cidade': cidade,
                'estado': estado
            })
            if response.status_code == 200:
                return redirect('painel:listar_clinicas')
        except Exception as e:
            return redirect('painel:cadastrar_clinica', {'message': f'Erro ao cadastrar clínica: {str(e)}'})
    return render(request, 'painel/cadastrar_clinica.html', {'estados': estados})


def listar_clinicas(request):
    url_clinicas = f'{base_url}/clinicas/'
    url_estados = f'{base_url}/estados/'
    clinicas = requests.get(url_clinicas).json()
    estados = requests.get(url_estados).json()
    return render(request, 'painel/listar_clinicas.html', {'clinicas': clinicas, 'estados': estados})


def editar_clinica(request, id):
    url_clinica_id = f'{base_url}/clinicas/{id}/'
    clinica_id = requests.get(url_clinica_id).json()
    
    if request.method == 'POST':
        # Processar o formulário
        nome = request.POST.get('nome')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')
        celular = request.POST.get('celular')
        celular2 = request.POST.get('celular2')
        cnpj = request.POST.get('cnpj')
        email = request.POST.get('email')
        try:
            response = requests.put(url_clinica_id, json={
                'nome': nome,
                'cep': cep,
                'rua': rua,
                'numero': numero,
                'bairro': bairro,
                'cidade': cidade,
                'estado': estado,
                'celular': celular,
                'celular2': celular2,
                'cnpj': cnpj,
                'email': email
            })
            if response.status_code == 200:
                return redirect('painel:listar_clinicas')
        except Exception as e:
            return redirect('painel:listar_clinicas')
            
    return render(request, 'painel:listar_clinicas', {'clinica': clinica_id})


def excluir_clinica(request, id):
    url_clinica_id = f'{base_url}/clinicas/{id}/'
    response = requests.delete(url_clinica_id)
    if response.status_code == 200:
        return redirect('painel:listar_clinicas')
    return redirect('painel:listar_clinicas')

## CRUD Salas


def listar_salas(request):
    url_clinicas = f'{base_url}/clinicas/'
    
    clinicas = requests.get(url_clinicas).json()
    clinica_selecionada = request.GET.get('clinica')

    url_salas_by_clinica_id = f'{base_url}/salas/clinica/{clinica_selecionada}'
    
    
    if clinica_selecionada:
        salas = requests.get(url_salas_by_clinica_id).json()
    else: 
        salas = None
    return render(request, 'painel/listar_salas.html', {
        'salas': salas, 
        'clinicas': clinicas,
        'clinica_selecionada': clinica_selecionada
    })


def cadastrar_sala(request):
    url_salas = f'{base_url}/salas/'
    url_vagas = f'{base_url}/vagas/'
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        clinica_id = request.POST.get('clinica')

    if nome and clinica_id:
        response_salas = requests.post(url_salas, json={
            'nome': nome,
            'clinica': clinica_id
        })
        for i in range(1, 4):
            response_vagas = requests.post(url_vagas, json={
                'sala': response_salas.json()['id'],
                'clinica': clinica_id,
                "status": "disponivel",
                "turno": i,
                "segunda": None,
                "terca": None,
                "quarta": None,
                "quinta": None,
                "sexta": None,
                "max_pacientes": 25,
                "pacientes_atuais": 0

            })
        if response_salas.status_code == 200 and response_vagas.status_code == 200:
            return redirect(f'/painel/salas/?clinica={clinica_id}')

    return render(request, 'painel/cadastrar_sala.html')


def editar_sala(request, id):
    url = f'{base_url}/salas/{id}/'
    sala = requests.get(url).json()

    if request.method == 'POST':
        nome = request.POST.get('nome')

        response = requests.put(url, json={
            'nome': nome
        })
        
        if response.status_code == 200:
            # Redirecionar de volta para a página de listagem mantendo o filtro da clínica
            return redirect(f'/painel/salas/?clinica={sala["clinica"]}')
    
    return render(request, 'painel/editar_sala.html', {'sala': sala})


def excluir_sala(request, id):
    url = f'{base_url}/salas/{id}/'
    sala = requests.get(url).json()
    response = requests.delete(url)
    if response.status_code == 200:
        # Redirecionar de volta para a página de listagem mantendo o filtro da clínica
        return redirect(f'/painel/salas/?clinica={sala["clinica"]}')
    return redirect(f'/painel/salas/?clinica={sala["clinica"]}')

## CRUD Especialidades


def listar_especialidades(request):
    url = f'{base_url}/especialidades/'
    response = requests.get(url)
    especialidades = response.json()

    #especialidades = Especialidades.objects.all()
  
    return render(request, 'painel/listar_especialidades.html', {
        'especialidades': especialidades
    })


def cadastrar_especialidade(request):
    url = f'{base_url}/especialidades/'
    
    if request.method == 'POST':
        nome = request.POST.get('nome')

        if nome:
            response = requests.post(url, json={
                'nome': nome
            })
            if response.status_code == 200:
                return redirect(f'/painel/especialidades')
            else:
                return render(request, 'painel/cadastrar_especialidade.html', {'error': 'Erro ao cadastrar especialidade'})

    return render(request, 'painel/cadastrar_especialidade.html')


def editar_especialidade(request, id):
    url = f'{base_url}/especialidades/{id}/'
    
    # Buscar dados atuais da especialidade na API
    try:
        response = requests.get(url)
        if response.status_code == 200:
            especialidade_data = response.json()
            especialidade = {
                'id': especialidade_data.get('id'),
                'nome': especialidade_data.get('nome')
            }
        else:
            return redirect('painel:listar_especialidades')
    except requests.exceptions.RequestException:
        return redirect('painel:listar_especialidades')
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        
        if nome:
            try:
                response = requests.put(url, json={'nome': nome})
                if response.status_code == 200:
                    return redirect('painel:listar_especialidades')
                else:
                    return render(request, 'painel/editar_especialidade.html', {
                        'especialidade': especialidade, 
                        'error': f'Erro ao editar especialidade: Status {response.status_code}'
                    })
            except requests.exceptions.RequestException as e:
                return render(request, 'painel/editar_especialidade.html', {
                    'especialidade': especialidade, 
                    'error': f'Erro de conexão com API: {str(e)}'
                })
    
    return render(request, 'painel/editar_especialidade.html', {'especialidade': especialidade, 'error': 'Campo nome é obrigatório'})


def excluir_especialidade(request, id):
    url = f'{base_url}/especialidades/{id}/'
    try:
        response = requests.delete(url)
        if response.status_code == 200:
            return redirect('painel:listar_especialidades')
        else:
            return render(request, 'painel/listar_especialidades.html', {
                'error': f'Erro ao excluir especialidade: Status {response.status_code}'
            })
    except requests.exceptions.RequestException as e:
        return render(request, 'painel/listar_especialidades.html', {
            'error': f'Erro de conexão com API: {str(e)}'
        })

## CRUD Conselhos

def listar_conselhos(request):
    url = f'{base_url}/tipo-conselho/'
    response = requests.get(url)
    conselhos = response.json()

    return render(request, 'painel/listar_conselhos.html', {
        'conselhos': conselhos
    })


def cadastrar_conselho(request):
    url = f'{base_url}/tipo-conselho/'
    if request.method == 'POST':
        nome = request.POST.get('nome')

        if nome:
            response = requests.post(url, json={
                'nome': nome
            })
            if response.status_code == 200:
                return redirect('/painel/conselhos')
            else:
                return render(request, 'painel/cadastrar_conselho.html', {'error': 'Erro ao cadastrar conselho'})

    return render(request, 'painel/cadastrar_conselho.html')


def editar_conselho(request, id):
    url = f'{base_url}/tipo-conselho/{id}/'
    response = requests.get(url)
    conselho = response.json()

    if request.method == 'POST':
        nome = request.POST.get('nome')
        response = requests.put(url, json={
            'nome': nome
        })
        if response.status_code == 200:
            return redirect('/painel/conselhos')
        else:
            return render(request, 'painel/editar_conselho.html', {'conselho': conselho, 'error': 'Erro ao editar conselho'})
    
    return render(request, 'painel/editar_conselho.html', {'conselho': conselho})


def excluir_conselho(request, id):
    url = f'{base_url}/tipo-conselho/{id}/'
    try:
        
        response = requests.delete(url)
        if response.status_code == 200:
            return redirect('painel:listar_conselhos')
        else:
            return render(request, 'painel/listar_conselhos.html', {
                'error': f'Erro ao excluir conselho: Status {response.status_code}'})
    except requests.exceptions.RequestException as e:
        return render(request, 'painel/listar_conselhos.html', {
            'error': f'Erro de conexão com API: {str(e)}'
            })

## Estados

def listar_estados(request):
    url = f'{base_url}/estados/'
    response = requests.get(url)
    estados = response.json()

    return render(request, 'painel/listar_estados.html', {
        'estados': estados
    })


def cadastrar_estado(request):
    url = f'{base_url}/estados/'
    if request.method == 'POST':
        nome = request.POST.get('nome')
        uf = request.POST.get('uf')

        if nome and uf:
            response = requests.post(url, json={
                'nome': nome,
                'uf': uf
            })
            if response.status_code == 200:
                return redirect('/painel/estados')
            else:
                return render(request, 'painel/cadastrar_estado.html', {'error': 'Erro ao cadastrar estado'})

    return render(request, 'painel/cadastrar_estado.html')


def editar_estado(request, id):
    url = f'{base_url}/estados/{id}/'
    estado = requests.get(url).json()
    if request.method == 'POST':
        nome = request.POST.get('nome')
        uf = request.POST.get('uf')
        
        if nome and uf:
            response = requests.put(url, json={
                'nome': nome,
                'uf': uf
            })
            if response.status_code == 200:
                return redirect('/painel/estados')
            else:
                return render(request, 'painel/editar_estado.html', {'estado': estado, 'error': 'Erro ao editar estado'})
    
    return render(request, 'painel/editar_estado.html', {'estado': estado})


def excluir_estado(request, id):
    url = f'{base_url}/estados/{id}/'
    response = requests.delete(url)
    if response.status_code == 200:
        return redirect('/painel/estados')
    else:
        return render(request, 'painel/listar_estados.html', {'error': 'Erro ao excluir estado'})


def logout_view(request):
    logout(request)
    return redirect('login')