from django.urls import path
from . import views

app_name = 'presupuestos'

urlpatterns = [
    path('', views.presupuestos_lista, name='lista'),
    path('nuevo/', views.presupuesto_crear, name='crear'),
    path('<int:pk>/', views.presupuesto_detalle, name='detalle'),
    path('<int:pk>/item/', views.presupuesto_agregar_item, name='agregar_item'),
    path('<int:pk>/item/<int:item_pk>/eliminar/', views.presupuesto_eliminar_item, name='eliminar_item'),
    path('<int:pk>/estado/', views.presupuesto_cambiar_estado, name='cambiar_estado'),
    path('<int:pk>/pdf/',    views.presupuesto_pdf,           name='pdf'),
]
