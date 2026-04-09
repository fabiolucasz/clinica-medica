from django.contrib import admin
from .models import (
    Estados, Especialidades, Tipo_conselho, Clinicas, Salas, 
    Paciente, Medico, Vagas
)

# Models de configuração
@admin.register(Estados)
class EstadosAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'uf')
    search_fields = ('nome', 'uf')
    ordering = ('uf',)

@admin.register(Especialidades)
class EspecialidadesAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)
    ordering = ('nome',)

@admin.register(Tipo_conselho)
class Tipo_conselhoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)
    ordering = ('nome',)

# Models principais
@admin.register(Clinicas)
class ClinicasAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cnpj', 'celular', 'cidade', 'estado')
    search_fields = ('nome', 'cidade')
    list_filter = ('estado',)
    ordering = ('nome',)

@admin.register(Salas)
class SalasAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'clinica')
    search_fields = ('nome', 'clinica__nome')
    list_filter = ('clinica',)
    ordering = ('clinica', 'nome')

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cpf', 'celular', 'cidade')
    search_fields = ('nome', 'cpf', 'celular')
    list_filter = ('sexo', 'cidade')
    ordering = ('nome',)

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'especialidade', 'celular', 'cidade', 'valor_consulta')
    search_fields = ('nome', 'cpf', 'celular')
    list_filter = ('especialidade', 'sexo', 'cidade', 'tipo_conselho')
    ordering = ('nome',)
    readonly_fields = ('created_at',)

@admin.register(Vagas)
class VagasAdmin(admin.ModelAdmin):
    list_display = ('id', 'sala', 'clinica', 'turno', 'segunda', 'terca', 'quarta', 'quinta', 'sexta')
    search_fields = ('sala__nome', 'clinica__nome', 'turno')
    list_filter = ('clinica', 'turno', 'segunda', 'terca', 'quarta', 'quinta', 'sexta')
    ordering = ('clinica', 'sala', 'turno')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('sala', 'clinica', 'segunda', 'terca', 'quarta', 'quinta', 'sexta')
