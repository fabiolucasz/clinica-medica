from typing import Optional
from django.db import models



class Estados(models.Model):
    nome = models.CharField(unique=True,max_length=100)
    uf = models.CharField(unique=True,max_length=2)
    
    def __str__(self):
        return self.nome

class Especialidades(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nome
    
class Tipo_conselho(models.Model):
    nome = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
    def __str__(self):
        return self.nome

class Clinicas(models.Model):
    #Identificação
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, default='00.000.000/0000-00')
    email = models.EmailField()
    celular = models.CharField(max_length=20, default='0000000-0000')
    celular2 = models.CharField(max_length=20, blank=True, null=True)
    
    
    #Endereço
    cep = models.CharField(max_length=9)
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.ForeignKey(Estados, on_delete=models.CASCADE)
    
    
    #Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nome



class Paciente(models.Model):
    #Identificação
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    celular = models.CharField(max_length=20, unique=True)
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


    


class Medico(models.Model):
    #Identificação
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    celular = models.CharField(max_length=20, unique=True)
    cpf = models.CharField(unique=True,max_length=14)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=10)
    cep = models.CharField(max_length=9)


    #Endereço
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.ForeignKey(Estados, on_delete=models.CASCADE, related_name='estado')

    #Perfil
    foto_perfil = models.ImageField(upload_to='perfil', blank=True, null=True)
    especialidade = models.ForeignKey(Especialidades, on_delete=models.CASCADE, blank=True, null=True)
    rqe = models.CharField(max_length=20, blank=True, null=True, unique=True)
    valor_consulta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    role = models.CharField(default='medico')

    #documentos
    tipo_conselho = models.ForeignKey(Tipo_conselho, on_delete=models.CASCADE, blank=True, null=True)
    uf_conselho = models.ForeignKey(Estados, on_delete=models.CASCADE, blank=True, null=True, related_name='uf_conselho')
    numero_conselho = models.CharField(max_length=20, blank=True, null=True, unique=True)


    upload_arquivo = models.FileField(upload_to='arquivos', blank=True, null=True)
    
    #Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome



class Salas(models.Model):
    nome = models.CharField(max_length=100)
    clinica = models.ForeignKey(Clinicas, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.nome
    

class Vagas(models.Model):
    clinica = models.ForeignKey(Clinicas, on_delete=models.CASCADE)
    sala = models.ForeignKey(Salas, on_delete=models.CASCADE)
    
    status = models.CharField(max_length=10)
    turno = models.CharField(max_length=10)
    hora_inicio = models.TimeField(default='00:00')
    hora_fim = models.TimeField(default='23:59')
  
    segunda = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='segunda', blank=True, null=True)
    terca = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='terca', blank=True, null=True)
    quarta = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='quarta', blank=True, null=True)
    quinta = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='quinta', blank=True, null=True)
    sexta = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='sexta', blank=True, null=True)
    
    max_pacientes = models.IntegerField(default=25)
    pacientes_atuais = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['sala', 'turno']
    
    def __str__(self):
        return self.sala.nome + ' - ' + self.turno
    
class Agendamentos(models.Model):
    clinica = models.ForeignKey(Clinicas, on_delete=models.CASCADE)
    sala = models.ForeignKey(Salas, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    
    turno = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    
    def __str__(self):
        return self.paciente.nome + ' - ' + self.medico.nome + ' - ' + self.turno

