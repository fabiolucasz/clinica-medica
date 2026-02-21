from django.urls import path
from . import views

app_name = 'painel'
urlpatterns = [
    path("", views.index, name="index"),
    path("painel/", views.index, name="painel"),
    path("cadastrar-paciente/", views.cadastrar_paciente, name="cadastrar_paciente"),
    path('logout/', views.logout_view, name='logout'),
]