
from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView
from .views import dashboard
from django.contrib.auth import views as auth_views
from .views import (
    cadastrar_artesa,
    cadastrar_canal,
    cadastrar_feirante,
    cadastrar_agricultor,
)
from .views import relatorio_pdf
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.BASE, name='BASE'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('cadastro/artesa/', cadastrar_artesa, name='cadastrar_artesa'),
    path('lista/artesas/', views.listar_artesas, name='listar_artesas'),
    path('cadastro/canal/', cadastrar_canal, name='cadastrar_canal'),
    path('listar/canais/', views.listar_canais, name='listar_canais'),
    path('cadastro/feirante/', cadastrar_feirante, name='cadastrar_feirante'),
    path('listar/feirantes/', views.listar_feirantes, name='listar_feirantes'),
    path('cadastro/agricultor/', cadastrar_agricultor, name='cadastrar_agricultor'),
    path('lista/agricultores/', views.listar_agricultores, name='listar_agricultores'),

    path('eventos/cadastrar/', views.cadastrar_evento, name='cadastrar_evento'),
    path('eventos/', views.listar_eventos, name='listar_eventos'),
    path('eventos/<int:id>/visualizar/', views.visualizar_evento, name='visualizar_evento'),
    path('eventos/<int:id>/editar/', views.editar_evento, name='editar_evento'),
    path('eventos/<int:id>/excluir/', views.excluir_evento, name='excluir_evento'),

    path('relatorios/geral/', views.relatorio_geral, name='relatorio_geral'),
    path('relatorios/pdf/', views.relatorio_pdf, name='relatorio_pdf'),

    path('relatorio/pdf/', relatorio_pdf, name='relatorio_pdf'),

    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/novo/', views.adicionar_usuario, name='adicionar_usuario'),
    path('usuarios/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/excluir/<int:usuario_id>/', views.excluir_usuario, name='excluir_usuario'),
]


if settings.DEBUG is False:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)