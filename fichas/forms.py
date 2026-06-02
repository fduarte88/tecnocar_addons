from django import forms
from clientes.models import Cliente
from .models import Vehiculo, FichaIngreso
from accounts.models import Usuario


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = [
            'marca', 'placa', 'color', 'modelo', 'año', 'chassis',
            'km_entrada', 'km_salida',
            'acc_gato', 'acc_llave_rueda', 'acc_baliza', 'acc_extintor',
            'acc_compresor', 'acc_rueda_auxilio', 'acc_alfombras', 'acc_tuerca_seguridad',
        ]
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Toyota'}),
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: ABC 123'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Hilux'}),
            'año': forms.NumberInput(attrs={'class': 'form-control', 'min': 1950, 'max': 2030}),
            'chassis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nro. de chassis'}),
            'km_entrada': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'km_salida': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


class FichaIngresoForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.filter(activo=True).order_by('apellido', 'nombre'),
        required=True,
        label='Cliente',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'sel_cliente'}),
    )

    class Meta:
        model = FichaIngreso
        fields = ['vehiculo', 'fecha_ingreso', 'km_ingreso', 'fecha_estimada', 'solicitud']
        widgets = {
            'vehiculo': forms.Select(attrs={'class': 'form-select', 'id': 'sel_vehiculo'}),
            'fecha_ingreso': forms.DateTimeInput(
                attrs={'class': 'form-control flatpickr-dt', 'autocomplete': 'off',
                       'placeholder': 'DD/MM/AAAA HH:MM'},
                format='%d/%m/%Y %H:%M',
            ),
            'fecha_estimada': forms.DateInput(
                attrs={'class': 'form-control flatpickr-date', 'autocomplete': 'off',
                       'placeholder': 'DD/MM/AAAA'},
                format='%d/%m/%Y',
            ),
            'km_ingreso': forms.NumberInput(attrs={'class': 'form-control'}),
            'solicitud': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,
                                               'placeholder': 'Describa la solicitud del cliente...'}),
        }

    def __init__(self, *args, **kwargs):
        cliente_pk = kwargs.pop('cliente_pk', None)
        super().__init__(*args, **kwargs)

        # En modo edición: tomar el cliente del vehículo existente
        if self.instance.pk and self.instance.vehiculo_id:
            cliente_pk = self.instance.vehiculo.cliente_id
            self.fields['cliente'].initial = cliente_pk

        if cliente_pk:
            self.fields['cliente'].initial = cliente_pk
            self.fields['vehiculo'].queryset = Vehiculo.objects.filter(cliente_id=cliente_pk)
        else:
            self.fields['vehiculo'].queryset = Vehiculo.objects.none()

        # Formatear fecha con el formato visual DD/MM/YYYY HH:MM
        if self.instance.pk and self.instance.fecha_ingreso:
            self.initial['fecha_ingreso'] = self.instance.fecha_ingreso.strftime('%d/%m/%Y %H:%M')
