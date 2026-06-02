from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cedula', 'ruc', 'nombre', 'apellido', 'telefono', 'email', 'ciudad', 'direccion', 'requiere_factura']
        labels = {
            'cedula': 'Documento de Identidad Nro.',
        }
        widgets = {
            'cedula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 1.234.567', 'id': 'id_cedula'}),
            'ruc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 80012345-6'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0981-123456'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Asunción'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
