from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('painel/', include('painel.urls')),
    path('area-paciente/', include('area_paciente.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
