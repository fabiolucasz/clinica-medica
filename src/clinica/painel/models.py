from django.db import models

# Create your models here.
class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    celular = models.CharField(max_length=20)
    cpf = models.CharField(unique=True,max_length=14)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=10)
    cep = models.CharField(max_length=9)
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    role = models.CharField(default='paciente')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nome
