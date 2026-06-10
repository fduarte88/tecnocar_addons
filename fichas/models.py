from django.db import models
from django.utils import timezone
from clientes.models import Cliente
from accounts.models import Usuario


class Vehiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='vehiculos', verbose_name='Cliente')
    marca = models.CharField(max_length=50, verbose_name='Marca')
    modelo = models.CharField(max_length=50, verbose_name='Modelo')
    año = models.IntegerField(verbose_name='Año')
    placa = models.CharField(max_length=20, unique=True, verbose_name='Chapa')
    color = models.CharField(max_length=30, verbose_name='Color')
    chassis = models.CharField(max_length=50, blank=True, verbose_name='Chassis')
    km_entrada = models.IntegerField(default=0, verbose_name='Km Entrada')
    km_salida = models.IntegerField(default=0, verbose_name='Km Salida')

    # Accesorios
    acc_gato = models.BooleanField(default=False, verbose_name='Gato')
    acc_llave_rueda = models.BooleanField(default=False, verbose_name='Llave de Rueda')
    acc_baliza = models.BooleanField(default=False, verbose_name='Baliza')
    acc_extintor = models.BooleanField(default=False, verbose_name='Extintor')
    acc_compresor = models.BooleanField(default=False, verbose_name='Compresor')
    acc_rueda_auxilio = models.BooleanField(default=False, verbose_name='Rueda de Auxilio')
    acc_alfombras = models.BooleanField(default=False, verbose_name='Alfombras')
    acc_tuerca_seguridad = models.BooleanField(default=False, verbose_name='Tuerca de Seguridad')

    class Meta:
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'

    def __str__(self):
        return f'{self.marca} {self.modelo} ({self.placa})'

    @property
    def accesorios_presentes(self):
        campos = [
            ('acc_gato', 'Gato'),
            ('acc_llave_rueda', 'Llave de Rueda'),
            ('acc_baliza', 'Baliza'),
            ('acc_extintor', 'Extintor'),
            ('acc_compresor', 'Compresor'),
            ('acc_rueda_auxilio', 'Rueda de Auxilio'),
            ('acc_alfombras', 'Alfombras'),
            ('acc_tuerca_seguridad', 'Tuerca de Seguridad'),
        ]
        return [label for campo, label in campos if getattr(self, campo)]


class FichaIngreso(models.Model):
    ESTADO_CHOICES = [
        ('recibido', 'Recibido'),
        ('diagnostico', 'En Diagnóstico'),
        ('en_reparacion', 'En Reparación'),
        ('espera_repuestos', 'Espera de Repuestos'),
        ('listo', 'Listo para Entrega'),
        ('entregado', 'Entregado'),
    ]

    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='fichas', verbose_name='Vehículo')
    tecnico = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='fichas_asignadas', verbose_name='Técnico'
    )
    fecha_ingreso = models.DateTimeField(default=timezone.now, verbose_name='Fecha de Ingreso')
    fecha_estimada = models.DateField(null=True, blank=True, verbose_name='Fecha Estimada de Entrega')
    solicitud = models.TextField(verbose_name='Solicitud del Cliente', default='')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='recibido', verbose_name='Estado')
    km_ingreso = models.IntegerField(default=0, verbose_name='Km al Ingreso')

    class Meta:
        verbose_name = 'Hoja de Recepción'
        verbose_name_plural = 'Hojas de Recepción'
        ordering = ['-fecha_ingreso']

    def __str__(self):
        return f'HR-{self.pk:04d} | {self.vehiculo} - {self.get_estado_display()}'

    @property
    def estado_index(self):
        keys = [k for k, _ in self.ESTADO_CHOICES]
        return keys.index(self.estado)

    @property
    def estado_pct(self):
        n = len(self.ESTADO_CHOICES)
        return round(self.estado_index * (100.0 / n), 2)
