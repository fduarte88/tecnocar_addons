from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Presupuesto, ItemPresupuesto
from .forms import PresupuestoForm, ItemPresupuestoForm
from .pdf import generar_pdf_presupuesto


@login_required
def presupuestos_lista(request):
    presupuestos = Presupuesto.objects.select_related('ficha__vehiculo__cliente').order_by('-fecha')
    estado = request.GET.get('estado', '')
    if estado:
        presupuestos = presupuestos.filter(estado=estado)
    return render(request, 'presupuestos/lista.html', {
        'presupuestos': presupuestos, 'estado': estado,
        'estados': Presupuesto.ESTADO_CHOICES
    })


@login_required
def presupuesto_crear(request):
    from fichas.models import FichaIngreso
    if request.method == 'POST':
        ficha_pk      = request.POST.get('ficha')
        observaciones = request.POST.get('observaciones', '')
        cantidades    = request.POST.getlist('item_cantidad')
        descripciones = request.POST.getlist('item_descripcion')
        precios       = request.POST.getlist('item_precio')

        if ficha_pk:
            presupuesto = Presupuesto.objects.create(
                ficha_id=ficha_pk,
                observaciones=observaciones,
            )
            for cant, desc, precio in zip(cantidades, descripciones, precios):
                desc = desc.strip()
                if desc:
                    try:
                        p = int(str(precio).replace('.', '').replace(',', '') or 0)
                    except ValueError:
                        p = 0
                    try:
                        q = max(1, int(cant or 1))
                    except ValueError:
                        q = 1
                    ItemPresupuesto.objects.create(
                        presupuesto=presupuesto,
                        cantidad=q,
                        descripcion=desc,
                        precio=p,
                    )
            messages.success(request, f'Presupuesto P-{presupuesto.pk:04d} creado exitosamente.')
            return redirect('presupuestos:detalle', pk=presupuesto.pk)
        else:
            messages.error(request, 'Debe seleccionar una Hoja de Recepción.')

    fichas = FichaIngreso.objects.select_related(
        'vehiculo__cliente'
    ).exclude(estado='entregado').order_by('-fecha_ingreso')
    return render(request, 'presupuestos/form.html', {
        'fichas': fichas,
        'titulo': 'Nuevo Presupuesto',
    })


@login_required
def presupuesto_detalle(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    item_form = ItemPresupuestoForm()
    return render(request, 'presupuestos/detalle.html', {
        'presupuesto': presupuesto,
        'item_form': item_form,
    })


@login_required
def presupuesto_agregar_item(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    form = ItemPresupuestoForm(request.POST)
    if form.is_valid():
        item = form.save(commit=False)
        item.presupuesto = presupuesto
        item.save()
        messages.success(request, 'Item agregado.')
    return redirect('presupuestos:detalle', pk=pk)


@login_required
def presupuesto_eliminar_item(request, pk, item_pk):
    item = get_object_or_404(ItemPresupuesto, pk=item_pk, presupuesto__pk=pk)
    item.delete()
    messages.success(request, 'Item eliminado.')
    return redirect('presupuestos:detalle', pk=pk)


@login_required
def presupuesto_pdf(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    buffer = generar_pdf_presupuesto(presupuesto)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="P-{presupuesto.pk:04d}.pdf"'
    return response


@login_required
def presupuesto_editar_item(request, pk, item_pk):
    item = get_object_or_404(ItemPresupuesto, pk=item_pk, presupuesto__pk=pk)
    if request.method == 'POST' and item.presupuesto.estado == 'borrador':
        try:
            precio = int(str(request.POST.get('precio', '0')).replace('.', '').replace(',', '') or 0)
            item.precio = max(0, precio)
            item.save()
        except (ValueError, TypeError):
            messages.error(request, 'Precio inválido.')
    return redirect('presupuestos:detalle', pk=pk)


@login_required
def presupuesto_cambiar_estado(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    nuevo_estado = request.POST.get('estado')
    estados_validos = dict(Presupuesto.ESTADO_CHOICES)
    if nuevo_estado in estados_validos:
        presupuesto.estado = nuevo_estado
        presupuesto.save()
        messages.success(request, f'Estado actualizado a: {estados_validos[nuevo_estado]}')
    return redirect('presupuestos:detalle', pk=pk)
