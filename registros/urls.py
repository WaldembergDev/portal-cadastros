from django.urls import path
from . import views

urlpatterns = [
    path('', views.formulario_cadastro, name='formulario_cadastro'),
    path('listar_cadastros/', views.listar_cadastros, name='listar_cadastros'),
    path('visualizar_cadastro/<uuid:id>/', views.visualizar_cadastro, name='visualizar_cadastro'),
    path('visualizacao_kanban/', views.visualizacao_kanban, name='visualizacao_kanban'),
    path('atualizar_cadastro/<uuid:id>/', views.atualizar_cadastro, name='atualizar_cadastro'),
    path('disparar_emails/', views.disparar_emails, name='disparar_emails')
]