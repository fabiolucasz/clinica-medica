from django.db import models

# Create your models here.
class Paciente(models.Model):
    #Identificação
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    celular = models.CharField(max_length=20)
    cpf = models.CharField(unique=True,max_length=14)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=10)

    #Endereço
    cep = models.CharField(max_length=9)
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    #Perfil
    foto_perfil = models.ImageField(upload_to='perfil', blank=True, null=True)
    role = models.CharField(default='paciente')

    #Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nome

class Medico(models.Model):
    #Identificação
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    celular = models.CharField(max_length=20)
    cpf = models.CharField(unique=True,max_length=14)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=10)
    cep = models.CharField(max_length=9)


    #Endereço
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    #Perfil
    foto_perfil = models.ImageField(upload_to='perfil', blank=True, null=True)
    especialidade = models.CharField(max_length=100)
    valor_consulta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    role = models.CharField(default='medico')

    #documentos
    tipo_conselho = models.CharField(max_length=20, blank=True, null=True)
    uf_conselho = models.CharField(max_length=2, blank=True, null=True)
    numero_conselho = models.CharField(max_length=20, blank=True, null=True)
    upload_arquivo = models.FileField(upload_to='arquivos', blank=True, null=True)
    


    #Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


