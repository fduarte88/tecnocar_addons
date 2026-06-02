from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['cedula', 'nombre', 'apellido', 'telefono', 'email', 'activo']
    search_fields = ['cedula', 'nombre', 'apellido']
    list_filter = ['activo']
