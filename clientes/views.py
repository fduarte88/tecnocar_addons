from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Cliente
from .forms import ClienteForm


@login_required
def clientes_lista(request):
    q = request.GET.get('q', '')
    clientes = Cliente.objects.filter(activo=True)
    if q:
        clientes = clientes.filter(
            Q(nombre__icontains=q) | Q(apellido__icontains=q) | Q(cedula__icontains=q)
        )
    return render(request, 'clientes/lista.html', {'clientes': clientes, 'q': q})


@login_required
def cliente_crear(request):
    form = ClienteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        cliente = form.save()
        messages.success(request, f'Cliente {cliente} registrado. Ahora registre su vehículo.')
        return redirect('fichas:vehiculo_crear', cliente_pk=cliente.pk)
    return render(request, 'clientes/form.html', {'form': form, 'titulo': 'Nuevo Cliente'})


@login_required
def cliente_editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(request.POST or None, instance=cliente)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Cliente actualizado exitosamente.')
        return redirect('clientes:lista')
    return render(request, 'clientes/form.html', {'form': form, 'titulo': 'Editar Cliente', 'cliente': cliente})


@login_required
def cliente_detalle(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    vehiculos = cliente.vehiculos.all()
    return render(request, 'clientes/detalle.html', {'cliente': cliente, 'vehiculos': vehiculos})
