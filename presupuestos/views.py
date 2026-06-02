from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Presupuesto, ItemPresupuesto
from .forms import PresupuestoForm, ItemPresupuestoForm


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
    form = PresupuestoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        presupuesto = form.save()
        messages.success(request, 'Presupuesto creado exitosamente.')
        return redirect('presupuestos:detalle', pk=presupuesto.pk)
    return render(request, 'presupuestos/form.html', {'form': form, 'titulo': 'Nuevo Presupuesto'})


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
def presupuesto_cambiar_estado(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    nuevo_estado = request.POST.get('estado')
    estados_validos = dict(Presupuesto.ESTADO_CHOICES)
    if nuevo_estado in estados_validos:
        presupuesto.estado = nuevo_estado
        presupuesto.save()
        messages.success(request, f'Estado actualizado a: {estados_validos[nuevo_estado]}')
    return redirect('presupuestos:detalle', pk=pk)
