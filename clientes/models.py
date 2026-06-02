from django.db import models


class Cliente(models.Model):
    cedula = models.CharField(max_length=20, unique=True, verbose_name='Documento de Identidad Nro.')
    ruc = models.CharField(max_length=30, blank=True, verbose_name='RUC')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, verbose_name='Apellido')
    telefono = models.CharField(max_length=20, verbose_name='Teléfono')
    email = models.EmailField(blank=True, verbose_name='Email')
    ciudad = models.CharField(max_length=80, blank=True, verbose_name='Ciudad')
    direccion = models.TextField(blank=True, verbose_name='Dirección')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    requiere_factura = models.BooleanField(default=False, verbose_name='Requiere Factura')
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    @property
    def nombre_completo(self):
        return f'{self.nombre} {self.apellido}'
