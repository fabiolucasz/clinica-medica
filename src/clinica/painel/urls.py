from django.urls import path
from . import views

app_name = 'painel'
urlpatterns = [
    path("", views.index, name="index"),
    path("painel/", views.index, name="painel"),
    path("cadastrar-paciente/", views.cadastrar_paciente, name="cadastrar_paciente"),
    path("listar-pacientes/", views.listar_pacientes, name="listar_pacientes"),
    path("editar-paciente/<int:id>/", views.editar_paciente, name="editar_paciente"),
    path("excluir-paciente/<int:id>/", views.excluir_paciente, name="excluir_paciente"),
    path('logout/', views.logout_view, name='logout'),
]