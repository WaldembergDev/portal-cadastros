from django.urls import path
from . import views

urlpatterns = [
    path('', views.formulario_cadastro, name='formulario_cadastro'),
    path('listar_cadastros/', views.listar_cadastros, name='listar_cadastros')
]