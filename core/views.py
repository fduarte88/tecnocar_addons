from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from clientes.models import Cliente
from fichas.models import FichaIngreso
from presupuestos.models import Presupuesto


@login_required
def dashboard(request):
    total_clientes = Cliente.objects.filter(activo=True).count()
    total_fichas = FichaIngreso.objects.count()
    fichas_activas = FichaIngreso.objects.exclude(estado='entregado').count()
    total_presupuestos = Presupuesto.objects.count()
    presupuestos_aprobados = Presupuesto.objects.filter(estado='aprobado').count()

    fichas_recientes = FichaIngreso.objects.select_related('vehiculo__cliente').order_by('-fecha_ingreso')[:5]

    context = {
        'total_clientes': total_clientes,
        'total_fichas': total_fichas,
        'fichas_activas': fichas_activas,
        'total_presupuestos': total_presupuestos,
        'presupuestos_aprobados': presupuestos_aprobados,
        'fichas_recientes': fichas_recientes,
    }
    return render(request, 'core/dashboard.html', context)
