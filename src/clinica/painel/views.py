from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Paciente

# Create your views here.

@login_required
def index(request):
    return render(request, 'painel/painel.html')

@login_required
def cadastrar_paciente(request):
    """
    Cadastra um novo paciente
    """

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
        estado = request.POST.get('estado')
        
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
            estado=estado,
        )

        # Redirecionar para a lista de pacientes
        return redirect('painel:index')
        
    return render(request, 'painel/cadastrar_paciente.html')

@login_required
def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'painel/listar_pacientes.html', {'pacientes': pacientes})

@login_required
def editar_paciente(request, id):
    paciente = Paciente.objects.get(id=id)
    return render(request, 'painel/editar_paciente.html', {'paciente': paciente})

@login_required
def excluir_paciente(request, id):
    paciente = Paciente.objects.get(id=id)
    paciente.delete()
    return redirect('painel:listar_pacientes')

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