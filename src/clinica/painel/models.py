from typing import Optional
from django.db import models



class Estados(models.Model):
    nome = models.CharField(unique=True,max_length=100)
    uf = models.CharField(unique=True,max_length=2)
    
    def __str__(self):
        return self.nome



class Clinicas(models.Model):
    #Identificação
    nome = models.CharField(max_length=100)
    cep = models.CharField(max_length=9)
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.ForeignKey(Estados, on_delete=models.CASCADE)
    def __str__(self):
        return self.nome



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
    estado = models.ForeignKey(Estados, on_delete=models.CASCADE)

    #Perfil
    foto_perfil = models.ImageField(upload_to='perfil', blank=True, null=True)
    role = models.CharField(default='paciente')

    #Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nome

class Especialidades(models.Model):
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome
    
class Tipo_conselho(models.Model):
    nome = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
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
    estado = models.ForeignKey(Estados, on_delete=models.CASCADE)

    #Perfil
    foto_perfil = models.ImageField(upload_to='perfil', blank=True, null=True)
    especialidade = models.ForeignKey(Especialidades, on_delete=models.CASCADE)
    rqe = models.CharField(max_length=20, blank=True, null=True)
    valor_consulta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    role = models.CharField(default='medico')

    #Dias da semana e turno
    segunda = models.CharField(max_length=20, blank=True, null=True)
    terca = models.CharField(max_length=20, blank=True, null=True)
    quarta = models.CharField(max_length=20, blank=True, null=True)
    quinta = models.CharField(max_length=20, blank=True, null=True)
    sexta = models.CharField(max_length=20, blank=True, null=True)

    #Salas disponíveis

    #documentos
    tipo_conselho = models.ForeignKey(Tipo_conselho, on_delete=models.CASCADE, blank=True, null=True)
    uf_conselho = models.CharField(max_length=2, blank=True, null=True)
    numero_conselho = models.CharField(max_length=20, blank=True, null=True)
    upload_arquivo = models.FileField(upload_to='arquivos', blank=True, null=True)
    


    #Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome



class Salas(models.Model):
    nome = models.CharField(max_length=100)
    clinica = models.ForeignKey(Clinicas, on_delete=models.CASCADE)
    sublocador = models.ForeignKey(Medico, on_delete=models.CASCADE)
    segunda = models.CharField(max_length=100)
    terca = models.CharField(max_length=100)
    quarta = models.CharField(max_length=100)
    quinta = models.CharField(max_length=100)
    sexta = models.CharField(max_length=100)

    def __str__(self):
        return self.nome