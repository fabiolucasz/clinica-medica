from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'painel'
urlpatterns = [
    #Pacientes
    path("paciente/cadastrar/", views.cadastrar_paciente, name="cadastrar_paciente"),
    path("pacientes/", views.listar_pacientes, name="listar_pacientes"),
    path("paciente/editar/<int:id>/", views.editar_paciente, name="editar_paciente"),
    path("paciente/excluir/<int:id>/", views.excluir_paciente, name="excluir_paciente"),

    #Medicos
    path("medicos/", views.listar_medicos, name="listar_medicos"),
    path("medico/detalhes/<int:id>/", views.medico_detalhes, name="medico_detalhes"),
    path("medico/cadastrar/", views.cadastrar_medico, name="cadastrar_medico"),
    path("cadastrar-medico-sala/<int:medico_id>/", views.cadastrar_medico_sala, name="cadastrar_medico_sala"),

    #Consultas
    path("consulta/agendar/", views.agendar_consulta, name="agendar_consulta"),
    path("buscar-pacientes/", views.buscar_pacientes, name="buscar_pacientes"),
    path("consultas/", views.listar_consultas, name="listar_consultas"),
    path("consulta/editar/<int:id>/", views.editar_consulta, name="editar_consulta"),

    #Configurações

    ## Clinica
    path("clinicas/", views.listar_clinicas, name="listar_clinicas"),
    path("clinica/cadastrar/", views.cadastrar_clinica, name="cadastrar_clinica"),
    path("clinica/editar/<int:id>/", views.editar_clinica, name="editar_clinica"),
    path("clinica/excluir/<int:id>/", views.excluir_clinica, name="excluir_clinica"),

    ## Salas
    path("salas/", views.listar_salas, name="listar_salas"),
    path("sala/cadastrar/", views.cadastrar_sala, name="cadastrar_sala"),
    path("sala/editar/<int:id>/", views.editar_sala, name="editar_sala"),
    path("sala/excluir/<int:id>/", views.excluir_sala, name="excluir_sala"),

    ## Especialidades
    path("especialidades/", views.listar_especialidades, name="listar_especialidades"),
    path("especialidade/cadastrar/", views.cadastrar_especialidade, name="cadastrar_especialidade"),
    path("especialidade/editar/<int:id>/", views.editar_especialidade, name="editar_especialidade"),
    path("especialidade/excluir/<int:id>/", views.excluir_especialidade, name="excluir_especialidade"),

    ## Conselhos
    path("conselhos/", views.listar_conselhos, name="listar_conselhos"),
    path("conselho/cadastrar/", views.cadastrar_conselho, name="cadastrar_conselho"),
    path("conselho/editar/<int:id>/", views.editar_conselho, name="editar_conselho"),
    path("conselho/excluir/<int:id>/", views.excluir_conselho, name="excluir_conselho"),

    ## Estados
    path("estados/", views.listar_estados, name="listar_estados"),
    path("estado/cadastrar/", views.cadastrar_estado, name="cadastrar_estado"),
    path("estado/editar/<int:id>/", views.editar_estado, name="editar_estado"),
    path("estado/excluir/<int:id>/", views.excluir_estado, name="excluir_estado"),

    path('logout/', views.logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)