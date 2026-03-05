from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'painel'
urlpatterns = [
    path("", views.index, name="index"),
    path("painel/", views.index, name="painel"),
    #Pacientes
    path("cadastrar-paciente/", views.cadastrar_paciente, name="cadastrar_paciente"),
    path("listar-pacientes/", views.listar_pacientes, name="listar_pacientes"),
    path("editar-paciente/<int:id>/", views.editar_paciente, name="editar_paciente"),
    path("excluir-paciente/<int:id>/", views.excluir_paciente, name="excluir_paciente"),

    #Medicos
    path("medicos/", views.listar_medicos, name="listar_medicos"),
    path("cadastrar-medico/", views.cadastrar_medico, name="cadastrar_medico"),
    path("medico/detalhes/<int:id>/", views.medico_detalhes, name="medico_detalhes"),

    path('logout/', views.logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)