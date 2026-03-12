from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Paciente, Medico, Tipo_conselho, Estados, Clinicas
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
        especialidade = request.POST.get('especialidade')
        tipo_conselho = request.POST.get('tipo_conselho')
        uf_conselho = request.POST.get('uf_conselho')
        numero_conselho = request.POST.get('numero_conselho')
        rqe = request.POST.get('rqe')
        valor_consulta = request.POST.get('valor_consulta')
        upload_documento = request.FILES.get('upload_documento')

        data_cadastro = datetime.now()
        
        
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
            estado=estado,

            foto_perfil=foto_perfil,
            especialidade=especialidade,
            tipo_conselho=tipo_conselho,
            uf_conselho=uf_conselho,
            numero_conselho=numero_conselho,
            rqe=rqe,
            valor_consulta=valor_consulta,
            upload_documento=upload_documento,
            data_cadastro=data_cadastro
        )


        
        return render(request, 'painel/cadastrar_medico.html')
    
    return render(request, 'painel/cadastrar_medico.html', {'tipo_conselho': tipo_conselho, 'estados': estados, 'clinicas': clinicas})

@login_required
def listar_medicos(request):
    medicos = Medico.objects.all()
    return render(request, 'painel/medicos.html', {'medicos': medicos})

@login_required
def medico_detalhes(request, id):
    medico = get_object_or_404(Medico, pk=id)
    return render(request, 'painel/medico_detalhes.html', {'medico': medico})

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