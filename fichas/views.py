import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .pdf import generar_pdf_hoja_recepcion
from clientes.models import Cliente
from .models import FichaIngreso, Vehiculo
from .forms import FichaIngresoForm, VehiculoForm

ACCESORIOS_CAMPOS = [
    ('acc_gato',           'Gato'),
    ('acc_llave_rueda',    'Llave de Rueda'),
    ('acc_baliza',         'Baliza'),
    ('acc_extintor',       'Extintor'),
    ('acc_compresor',      'Compresor'),
    ('acc_rueda_auxilio',  'Rueda de Auxilio'),
    ('acc_alfombras',      'Alfombras'),
    ('acc_tuerca_seguridad', 'Tuerca de Seguridad'),
]


@login_required
def fichas_lista(request):
    fichas = FichaIngreso.objects.select_related('vehiculo__cliente', 'tecnico').order_by('-fecha_ingreso')
    estado = request.GET.get('estado', '')
    if estado:
        fichas = fichas.filter(estado=estado)
    return render(request, 'fichas/lista.html', {'fichas': fichas, 'estado': estado,
                                                  'estados': FichaIngreso.ESTADO_CHOICES})


@login_required
def api_vehiculos_cliente(request, cliente_pk):
    vehiculos = Vehiculo.objects.filter(cliente_id=cliente_pk).order_by('marca', 'modelo')
    data = [_vehiculo_dict(v) for v in vehiculos]
    return JsonResponse(data, safe=False)


def _vehiculo_dict(v):
    d = {
        'id': v.id,
        'texto': f'{v.marca} {v.modelo} — {v.placa}',
        'marca': v.marca,
        'modelo': v.modelo,
        'placa': v.placa,
        'año': v.año,
        'color': v.color,
        'chassis': v.chassis or '—',
        'km_entrada': v.km_entrada,
        'km_salida': v.km_salida,
        'accesorios': v.accesorios_presentes,
    }
    for campo, _ in ACCESORIOS_CAMPOS:
        d[campo] = getattr(v, campo)
    return d


def _vehiculos_json(cliente_pk):
    vehiculos = Vehiculo.objects.filter(cliente_id=cliente_pk).order_by('marca', 'modelo')
    return json.dumps([_vehiculo_dict(v) for v in vehiculos])


def _guardar_accesorios(vehiculo, post_data):
    for campo, _ in ACCESORIOS_CAMPOS:
        setattr(vehiculo, campo, campo in post_data)
    vehiculo.save(update_fields=[c for c, _ in ACCESORIOS_CAMPOS])


@login_required
def ficha_crear(request):
    # En POST, el cliente viene del campo del formulario; en GET viene del parámetro URL
    if request.method == 'POST':
        cliente_pk = request.POST.get('cliente') or ''
    else:
        cliente_pk = request.GET.get('cliente') or ''

    form = FichaIngresoForm(request.POST or None, cliente_pk=cliente_pk or None)

    if request.method == 'POST' and form.is_valid():
        ficha = form.save()
        _guardar_accesorios(ficha.vehiculo, request.POST)
        messages.success(request, 'Hoja de Recepción registrada exitosamente.')
        return redirect('fichas:detalle', pk=ficha.pk)

    vehiculos_json = _vehiculos_json(cliente_pk) if cliente_pk else '[]'
    clientes = Cliente.objects.filter(activo=True).order_by('apellido', 'nombre')
    return render(request, 'fichas/form.html', {
        'form': form,
        'titulo': 'Nueva Hoja de Recepción',
        'clientes': clientes,
        'cliente_pk': cliente_pk,
        'vehiculo_pk': request.POST.get('vehiculo', ''),
        'vehiculos_json': vehiculos_json,
        'accesorios_campos': ACCESORIOS_CAMPOS,
    })


@login_required
def ficha_detalle(request, pk):
    ficha = get_object_or_404(FichaIngreso, pk=pk)
    return render(request, 'fichas/detalle.html', {'ficha': ficha})


@login_required
def ficha_editar(request, pk):
    ficha = get_object_or_404(FichaIngreso, pk=pk)
    form = FichaIngresoForm(request.POST or None, instance=ficha)
    cliente_pk = ficha.vehiculo.cliente_id

    if request.method == 'POST' and form.is_valid():
        ficha = form.save()
        _guardar_accesorios(ficha.vehiculo, request.POST)
        messages.success(request, 'Hoja de Recepción actualizada exitosamente.')
        return redirect('fichas:detalle', pk=pk)

    vehiculos_json = _vehiculos_json(cliente_pk)
    clientes = Cliente.objects.filter(activo=True).order_by('apellido', 'nombre')
    return render(request, 'fichas/form.html', {
        'form': form,
        'titulo': 'Editar Hoja de Recepción',
        'ficha': ficha,
        'clientes': clientes,
        'cliente_pk': str(cliente_pk),
        'vehiculo_pk': str(ficha.vehiculo_id),
        'vehiculos_json': vehiculos_json,
        'accesorios_campos': ACCESORIOS_CAMPOS,
    })


@login_required
def vehiculo_crear(request, cliente_pk):
    cliente = get_object_or_404(Cliente, pk=cliente_pk)
    form = VehiculoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        vehiculo = form.save(commit=False)
        vehiculo.cliente = cliente
        vehiculo.save()
        messages.success(request, f'Vehículo {vehiculo.placa} registrado para {cliente}.')
        return redirect('clientes:detalle', pk=cliente_pk)
    return render(request, 'fichas/vehiculo_form.html', {
        'form': form,
        'cliente': cliente,
        'titulo': f'Registrar Vehículo — {cliente}',
    })


@login_required
def vehiculo_editar(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    form = VehiculoForm(request.POST or None, instance=vehiculo)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Vehículo actualizado.')
        return redirect('clientes:detalle', pk=vehiculo.cliente.pk)
    return render(request, 'fichas/vehiculo_form.html', {
        'form': form,
        'cliente': vehiculo.cliente,
        'titulo': f'Editar Vehículo — {vehiculo.placa}',
        'vehiculo': vehiculo,
    })


@login_required
def ficha_pdf(request, pk):
    ficha = get_object_or_404(FichaIngreso, pk=pk)
    buffer = generar_pdf_hoja_recepcion(ficha)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="HR-{ficha.pk:04d}.pdf"'
    return response


@login_required
def ficha_cambiar_estado(request, pk):
    ficha = get_object_or_404(FichaIngreso, pk=pk)
    nuevo_estado = request.POST.get('estado')
    estados_validos = dict(FichaIngreso.ESTADO_CHOICES)
    if nuevo_estado in estados_validos:
        ficha.estado = nuevo_estado
        ficha.save()
        messages.success(request, f'Estado actualizado a: {estados_validos[nuevo_estado]}')
    return redirect('fichas:detalle', pk=pk)
