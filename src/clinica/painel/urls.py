from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'painel'
urlpatterns = [
    #Pacientes
    path("cadastrar-paciente/", views.cadastrar_paciente, name="cadastrar_paciente"),
    path("listar-pacientes/", views.listar_pacientes, name="listar_pacientes"),
    path("editar-paciente/<int:id>/", views.editar_paciente, name="editar_paciente"),
    path("excluir-paciente/<int:id>/", views.excluir_paciente, name="excluir_paciente"),

    #Medicos
    path("medicos/", views.listar_medicos, name="listar_medicos"),
    path("medico/detalhes/<int:id>/", views.medico_detalhes, name="medico_detalhes"),
    path("cadastrar-medico/", views.cadastrar_medico, name="cadastrar_medico"),
    path("cadastrar-medico-sala/<int:medico_id>/", views.cadastrar_medico_sala, name="cadastrar_medico_sala"),

    #Consultas
    path("agendar-consulta/", views.agendar_consulta, name="agendar_consulta"),
    path("buscar-pacientes/", views.buscar_pacientes, name="buscar_pacientes"),
    path("listar-consultas/", views.listar_consultas, name="listar_consultas"),
    path("editar-consulta/<int:id>/", views.editar_consulta, name="editar_consulta"),
    
    #Configurações
    
    ## Clinica
    path("config/", views.config, name="config"),
    path("config-clinicas/", views.listar_clinicas, name="listar_clinicas"),
    path("cadastrar-clinica/", views.cadastrar_clinica, name="cadastrar_clinica"),
    path("editar-clinica/<int:id>/", views.editar_clinica, name="editar_clinica"),
    path("excluir-clinica/<int:id>/", views.excluir_clinica, name="excluir_clinica"),
    
    ## Salas
    path("config-salas/", views.listar_salas, name="listar_salas"),
    path("cadastrar-sala/", views.cadastrar_sala, name="cadastrar_sala"),
    path("editar-sala/<int:id>/", views.editar_sala, name="editar_sala"),
    path("excluir-sala/<int:id>/", views.excluir_sala, name="excluir_sala"),

    path('logout/', views.logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)