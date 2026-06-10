from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from .models import Usuario
from .forms import LoginForm, UsuarioCreacionForm, UsuarioEdicionForm, CambiarPasswordForm


def es_admin(user):
    return user.is_authenticated and (user.is_superuser or user.rol == 'admin')


@ratelimit(key='ip', rate='100/m', method='POST', block=True)
def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect(request.GET.get('next', 'core:dashboard'))
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
@user_passes_test(es_admin)
def usuarios_lista(request):
    usuarios = Usuario.objects.all().order_by('username')
    return render(request, 'accounts/usuarios_lista.html', {'usuarios': usuarios})


@login_required
@user_passes_test(es_admin)
def usuario_crear(request):
    form = UsuarioCreacionForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Usuario creado exitosamente.')
        return redirect('accounts:usuarios_lista')
    return render(request, 'accounts/usuario_form.html', {'form': form, 'titulo': 'Nuevo Usuario'})


@login_required
@user_passes_test(es_admin)
def usuario_editar(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    form = UsuarioEdicionForm(request.POST or None, request.FILES or None, instance=usuario)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Usuario actualizado exitosamente.')
        return redirect('accounts:usuarios_lista')
    return render(request, 'accounts/usuario_form.html', {'form': form, 'titulo': 'Editar Usuario', 'usuario': usuario})


@login_required
@user_passes_test(es_admin)
def usuario_cambiar_password(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    form = CambiarPasswordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        usuario.set_password(form.cleaned_data['password1'])
        usuario.save()
        messages.success(request, 'Contraseña actualizada exitosamente.')
        return redirect('accounts:usuarios_lista')
    return render(request, 'accounts/usuario_password.html', {'form': form, 'usuario': usuario})


@login_required
@user_passes_test(es_admin)
def usuario_toggle_activo(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if usuario != request.user:
        usuario.is_active = not usuario.is_active
        usuario.save()
        estado = 'activado' if usuario.is_active else 'desactivado'
        messages.success(request, f'Usuario {estado} exitosamente.')
    else:
        messages.warning(request, 'No puede desactivar su propio usuario.')
    return redirect('accounts:usuarios_lista')
