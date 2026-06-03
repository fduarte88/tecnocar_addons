from django.contrib import admin
from .models import Presupuesto, ItemPresupuesto


class ItemInline(admin.TabularInline):
    model = ItemPresupuesto
    fields = ['descripcion', 'precio']
    extra = 0


@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'ficha', 'estado', 'fecha']
    list_filter = ['estado']
    inlines = [ItemInline]
