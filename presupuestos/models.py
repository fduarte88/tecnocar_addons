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

    PASOS_LINEALES = ['borrador', 'enviado', 'aprobado', 'facturado']

    def __str__(self):
        return f'P-{self.pk:04d} | {self.ficha.vehiculo}'

    @property
    def total(self):
        return sum(item.total for item in self.items.all())

    @property
    def pasos_lineales(self):
        labels = dict(self.ESTADO_CHOICES)
        return [(v, labels[v]) for v in self.PASOS_LINEALES]

    @property
    def estado_index(self):
        if self.estado not in self.PASOS_LINEALES:
            return -1
        return self.PASOS_LINEALES.index(self.estado)

    @property
    def estado_pct(self):
        if self.estado_index < 0:
            return 0
        n = len(self.PASOS_LINEALES)
        return round(self.estado_index * (100.0 / n), 2)


class ItemPresupuesto(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE, related_name='items', verbose_name='Presupuesto')
    cantidad = models.IntegerField(default=1, verbose_name='Cantidad')
    descripcion = models.CharField(max_length=300, verbose_name='Descripción del Trabajo')
    precio = models.BigIntegerField(default=0, verbose_name='Precio Unitario (₲)')

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ['pk']

    @property
    def total(self):
        return self.cantidad * self.precio

    def __str__(self):
        return self.descripcion
