from django.contrib import admin
from .models import Vehiculo, FichaIngreso


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ['placa', 'cliente', 'marca', 'modelo', 'año', 'color']
    search_fields = ['placa', 'marca', 'modelo']


@admin.register(FichaIngreso)
class FichaIngresoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'vehiculo', 'estado', 'tecnico', 'fecha_ingreso']
    list_filter = ['estado']
    search_fields = ['vehiculo__placa']
