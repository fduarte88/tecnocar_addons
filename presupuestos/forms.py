from django import forms
from .models import Presupuesto, ItemPresupuesto


class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['ficha', 'observaciones']
        widgets = {
            'ficha': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class ItemPresupuestoForm(forms.ModelForm):
    class Meta:
        model = ItemPresupuesto
        fields = ['descripcion', 'precio']
        widgets = {
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del trabajo o repuesto...',
                'id': 'id_item_descripcion',
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control text-end',
                'placeholder': '0',
                'min': '0',
                'id': 'id_item_precio',
            }),
        }
