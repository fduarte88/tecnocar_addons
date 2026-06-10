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
        fields = ['cantidad', 'descripcion', 'precio']
        widgets = {
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control text-center',
                'placeholder': '1',
                'min': '1',
                'id': 'id_item_cantidad',
            }),
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
