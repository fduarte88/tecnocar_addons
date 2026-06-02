from django import forms
from .models import Presupuesto, ItemPresupuesto


class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['ficha', 'observaciones']
        widgets = {
            'ficha': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ItemPresupuestoForm(forms.ModelForm):
    class Meta:
        model = ItemPresupuesto
        fields = ['descripcion', 'cantidad', 'precio_unitario']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción del servicio o repuesto'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }
