from django.db import models
from fichas.models import FichaIngreso


class Presupuesto(models.Model):
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('enviado', 'Enviado'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
        ('facturado', 'Facturado'),
    ]

    ficha = models.ForeignKey(FichaIngreso, on_delete=models.CASCADE, related_name='presupuestos', verbose_name='Hoja de Recepción')
    fecha = models.DateField(auto_now_add=True, verbose_name='Fecha')
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='borrador', verbose_name='Estado')
    observaciones = models.TextField(blank=True, verbose_name='Observaciones')

    class Meta:
        verbose_name = 'Presupuesto'
        verbose_name_plural = 'Presupuestos'
        ordering = ['-fecha']

    def __str__(self):
        return f'P-{self.pk:04d} | {self.ficha.vehiculo}'

    @property
    def subtotal(self):
        return sum(item.total for item in self.items.all())

    @property
    def iva(self):
        return self.subtotal * 16 / 100

    @property
    def total(self):
        return self.subtotal + self.iva


class ItemPresupuesto(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE, related_name='items', verbose_name='Presupuesto')
    descripcion = models.CharField(max_length=200, verbose_name='Descripción')
    cantidad = models.DecimalField(max_digits=8, decimal_places=2, default=1, verbose_name='Cantidad')
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Precio Unitario')

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    @property
    def total(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return self.descripcion
