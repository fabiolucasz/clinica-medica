from datetime import datetime
import json
from struct import pack
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.serializers import serialize
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


def cadastrar_medico(request):
    tipo_conselho = Tipo_conselho.objects.all()
    clinicas = Clinicas.objects.all()
    estados = Estados.objects.all()
    especialidades = Especialidades.objects.all()
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

        foto_perfil = request.FILES.get('foto_perfil')
        especialidade = request.POST.get('especialidade_id')
        tipo_conselho = request.POST.get('tipo_conselho_id')
        uf_conselho = request.POST.get('uf_conselho_id')
        numero_conselho = request.POST.get('numero_conselho')
        rqe = request.POST.get('rqe')
        valor_consulta = request.POST.get('valor_consulta')
        upload_documento = request.FILES.get('upload_documento')

        data_cadastro = datetime.now()
        
        # Buscar instâncias dos objetos relacionados
        estado_obj = get_object_or_404(Estados, id=estado)
        especialidade_obj = get_object_or_404(Especialidades, id=especialidade)
        tipo_conselho_obj = get_object_or_404(Tipo_conselho, id=tipo_conselho)
        uf_conselho_obj = get_object_or_404(Estados, id=uf_conselho)
        
        try:
            # Criar o medico
            medico = Medico.objects.create(
                nome=nome,
                email=email,
                celular=celular,
                cpf=cpf,
                data_nascimento=data_nascimento,
                sexo=sexo,
                cep=cep,
                rua=rua,
                numero=numero,
                bairro=bairro,
                cidade=cidade,
                estado=estado_obj,

                foto_perfil=foto_perfil,
                especialidade=especialidade_obj,
                tipo_conselho=tipo_conselho_obj,
                uf_conselho=uf_conselho_obj,
                numero_conselho=numero_conselho,
                rqe=rqe,
                valor_consulta=valor_consulta,
                upload_arquivo=upload_documento,
            )
            
            # Redirecionar para a página de seleção de vagas com o ID do médico
            return redirect('painel:cadastrar_medico_sala', medico_id=medico.id)
            
        except Exception as e:
            # Tratar erro de email duplicado
            if "UNIQUE constraint failed: painel_medico.email" in str(e):
                error_message = "Este e-mail já está cadastrado. Por favor, use outro e-mail."
            elif "UNIQUE constraint failed: painel_medico.cpf" in str(e):
                error_message = "Este CPF já está cadastrado. Por favor, verifique os dados."
            elif "UNIQUE constraint failed: painel_medico.celular" in str(e):
                error_message = "Este celular já está cadastrado. Por favor, use outro número."
            else:
                error_message = f"Erro ao cadastrar médico: {str(e)}"
            
            return render(request, 'painel/cadastrar_medico.html', {
                'tipo_conselho': tipo_conselho,
                'especialidades': especialidades,
                'estados': estados,
                'clinicas': clinicas,
                'error': error_message
            })
    
    return render(request, 'painel/cadastrar_medico.html', {'tipo_conselho': tipo_conselho,'especialidades': especialidades, 'estados': estados, 'clinicas': clinicas})


def cadastrar_medico_sala(request, medico_id):
    # Buscar o médico cadastrado
    medico = get_object_or_404(Medico, id=medico_id)
    
    clinicas = Clinicas.objects.all()
    salas = Salas.objects.all()
    vagas = Vagas.objects.select_related('segunda', 'terca', 'quarta', 'quinta', 'sexta').all()
    
    # Serializar vagas para JSON
    vagas_data = []
    for vaga in vagas:
        vaga_dict = {
            'id': vaga.id,
            'sala_id': vaga.sala_id,
            'turno': vaga.turno,
            'segunda': vaga.segunda.nome if vaga.segunda else None,
            'terca': vaga.terca.nome if vaga.terca else None,
            'quarta': vaga.quarta.nome if vaga.quarta else None,
            'quinta': vaga.quinta.nome if vaga.quinta else None,
            'sexta': vaga.sexta.nome if vaga.sexta else None,
        }
        vagas_data.append(vaga_dict)
    
    if request.method == 'POST':
        # Processar as vagas selecionadas
        clinica_id = request.POST.get('clinica')
        sala_id = request.POST.get('sala')
        
        # Buscar instâncias dos objetos relacionados
        clinica_obj = get_object_or_404(Clinicas, id=clinica_id)
        sala_obj = get_object_or_404(Salas, id=sala_id)
        
        # Processar checkboxes selecionados
        for key, value in request.POST.items():
            if key.startswith('vaga_') and value:
                # Extrair informações do checkbox
                parts = key.split('_')
                vaga_id = parts[1]
                dia = parts[2]
                
                # Buscar a vaga
                vaga = get_object_or_404(Vagas, id=vaga_id)
                
                # Atualizar o campo do dia com o médico
                if dia == 'segunda':
                    vaga.segunda = medico
                elif dia == 'terca':
                    vaga.terca = medico
                elif dia == 'quarta':
                    vaga.quarta = medico
                elif dia == 'quinta':
                    vaga.quinta = medico
                elif dia == 'sexta':
                    vaga.sexta = medico
                
                vaga.save()
        
        return redirect('painel:listar_medicos')
    
    return render(request, 'painel/cadastrar_medico_sala.html', {
        'clinicas': clinicas, 
        'salas': salas, 
        'vagas': json.dumps(vagas_data),
        'medico': medico
    })



def listar_medicos(request):
    medicos = Medico.objects.all()
    return render(request, 'painel/medicos.html', {'medicos': medicos})


def medico_detalhes(request, id):
    medico = get_object_or_404(Medico, pk=id)
    
    # Buscar clínicas onde o médico tem vagas alocadas
    from django.db.models import Q
    clinicas_query = Vagas.objects.filter(
        Q(segunda=medico) | Q(terca=medico) | Q(quarta=medico) | 
        Q(quinta=medico) | Q(sexta=medico)
    ).values_list('clinica_id', flat=True).distinct()
    
    clinicas = Clinicas.objects.filter(id__in=clinicas_query)
    
    vagas = Vagas.objects.select_related('segunda', 'terca', 'quarta', 'quinta', 'sexta').all()
    
    return render(request, 'painel/medico_detalhes.html', {'medico': medico, 'clinicas': clinicas, 'vagas': vagas})


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
    url = f'{base_url}/salas/'
    if request.method == 'POST':
        nome = request.POST.get('nome')
        clinica_id = request.POST.get('clinica')

        if nome and clinica_id:
            response = requests.post(url, json={
                'nome': nome,
                'clinica': clinica_id
            })
            if response.status_code == 200:
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
    
    return render(request, 'painel/editar_especialidade.html', {'especialidade': especialidade})


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