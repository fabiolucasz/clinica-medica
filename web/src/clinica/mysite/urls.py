from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('api/check-token/', views.check_token, name='check_token'),
    path('admin/', admin.site.urls),
    path('painel/', include('painel.urls')),
    path('area-paciente/', include('area_paciente.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
