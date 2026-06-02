from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('recepcionista', 'Recepcionista'),
        ('tecnico', 'Técnico'),
    ]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='recepcionista', verbose_name='Rol')
    telefono = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Avatar')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_rol_display()})'

    @property
    def nombre_completo(self):
        return self.get_full_name() or self.username
