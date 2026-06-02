from django.urls import path
from . import views

app_name = 'fichas'

urlpatterns = [
    path('', views.fichas_lista, name='lista'),
    path('nueva/', views.ficha_crear, name='crear'),
    path('<int:pk>/', views.ficha_detalle, name='detalle'),
    path('<int:pk>/editar/', views.ficha_editar, name='editar'),
    path('<int:pk>/estado/', views.ficha_cambiar_estado, name='cambiar_estado'),
    path('vehiculo/nuevo/<int:cliente_pk>/', views.vehiculo_crear, name='vehiculo_crear'),
    path('vehiculo/<int:pk>/editar/', views.vehiculo_editar, name='vehiculo_editar'),
    path('api/cliente/<int:cliente_pk>/vehiculos/', views.api_vehiculos_cliente, name='api_vehiculos'),
    path('<int:pk>/pdf/', views.ficha_pdf, name='pdf'),
]
