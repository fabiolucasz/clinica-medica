from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from . import views

app_name = 'area_paciente'
urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('logout/', views.logout_view, name='logout'),
]