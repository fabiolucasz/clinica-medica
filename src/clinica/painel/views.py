from datetime import datetime
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Paciente, Medico, Tipo_conselho, Estados, Clinicas, Especialidades, Salas, Vagas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import webbrowser

@login_required
def index(request):
    return render(request, 'painel/painel.html')

# Views dos Pacientes
@login_required
def cadastrar_paciente(request):
    """
    Cadastra um novo paciente
    """
    estados = Estados.objects.all()

    # TODO: Implementar a verificação de CPF válido e preenchimento automático do campo de CEP, Mensagem de erro caso o CPF seja inválido ou já cadastrado.

    if request.method == 'POST':
        # Processar o formulário
        nome = request.POST.get('nome')
        celular = request.POST.get('celular')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        sexo = request.POST.get('sexo')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        estado_uf = request.POST.get('estado')
        
        # Buscar a instância de Estados pelo UF
        estado_obj = get_object_or_404(Estados, uf=estado_uf)
        
        # Criar o paciente
        paciente = Paciente.objects.create(
            nome=nome,
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
        )
        
        # Enviar mensagem de boas-vindas
        mensagem = f"Seja bem-vindo(a) a nossa clínica, {nome.upper()}! Estamos felizes em tê-lo(a) conosco."
        url = f'http://web.whatsapp.com/send?phone={celular}&text={mensagem}'       
        
        # Abrir URL no navegador padrão do usuário
        try:
            webbrowser.open(url, new=2)
        except Exception as e:
            print(f"Erro ao abrir navegador: {e}")
        
        # Redirecionar para a lista de pacientes
        return redirect('painel:index')
        
    return render(request, 'painel/cadastrar_paciente.html', {'estados': estados})

@login_required
def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'painel/listar_pacientes.html', {'pacientes': pacientes})

@login_required
def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, pk=id)
    
    if request.method == 'POST':
        # Processar o formulário
        paciente.nome = request.POST.get('nome')
        paciente.celular = request.POST.get('celular')
        paciente.cpf = request.POST.get('cpf')
        data_nascimento_obj = request.POST.get('data_nascimento')
        nascimento_iso = data_nascimento_obj.split('/')[2] + '-' + data_nascimento_obj.split('/')[1] + '-' + data_nascimento_obj.split('/')[0]
        paciente.data_nascimento = nascimento_iso
        paciente.sexo = request.POST.get('sexo')
        paciente.cep = request.POST.get('cep')
        paciente.rua = request.POST.get('rua')
        paciente.numero = request.POST.get('numero')
        paciente.bairro = request.POST.get('bairro')
        paciente.cidade = request.POST.get('cidade')
        estado_uf = request.POST.get('estado')
        
        # Buscar a instância de Estados pelo UF
        estado_obj = get_object_or_404(Estados, uf=estado_uf)
        paciente.estado = estado_obj
        
        paciente.save()
        mensagem_boas_vindas(request, paciente.celular, paciente.nome)
        
        return redirect('painel:listar_pacientes')
    
    return redirect('painel:listar_pacientes')

@login_required
def excluir_paciente(request, id):
    paciente = get_object_or_404(Paciente, pk=id)
    paciente.delete()
    return redirect('painel:listar_pacientes')


#Views dos Médicos

@login_required
def cadastrar_medico(request):
    tipo_conselho = Tipo_conselho.objects.all()
    clinicas = Clinicas.objects.all()
    estados = Estados.objects.all()
    especialidades = Especialidades.objects.all()
    if request.method == 'POST':
        # Processar o formulário
        nome = request.POST.get('nome')
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
        
        # Criar o medico
        medico = Medico.objects.create(
            nome=nome,
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


@login_required
def listar_medicos(request):
    medicos = Medico.objects.all()
    return render(request, 'painel/medicos.html', {'medicos': medicos})

@login_required
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

@login_required
def agendar_consulta(request):
    return render(request, 'painel/agendar_consulta.html')

@login_required
def listar_consultas(request):
    return render(request, 'painel/listar_consultas.html')

@login_required
def editar_consulta(request, id):
    return render(request, 'painel/editar_consulta.html')

@login_required
def excluir_consulta(request, id):
    return render(request, 'painel/excluir_consulta.html')




@login_required
def logout_view(request):
    logout(request)
    return redirect('login')