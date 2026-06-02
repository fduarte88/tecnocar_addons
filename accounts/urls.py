from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('usuarios/', views.usuarios_lista, name='usuarios_lista'),
    path('usuarios/nuevo/', views.usuario_crear, name='usuario_crear'),
    path('usuarios/<int:pk>/editar/', views.usuario_editar, name='usuario_editar'),
    path('usuarios/<int:pk>/password/', views.usuario_cambiar_password, name='usuario_password'),
    path('usuarios/<int:pk>/toggle/', views.usuario_toggle_activo, name='usuario_toggle'),
]
