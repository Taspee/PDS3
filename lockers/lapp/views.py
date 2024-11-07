from django.shortcuts import render, get_object_or_404, redirect
from .models import Casillero, Usuario

# Vista para mostrar el estado de los casilleros
def casilleros_list(request):
    casilleros = Casillero.objects.select_related('usuario').all()  # Obtiene los casilleros con sus usuarios
    return render(request, 'casilleros_list.html', {'casilleros': casilleros})

from .forms import UsuarioForm  # Asegúrate de crear un formulario para Usuario

# Vista para listar usuarios
def usuarios_list(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios_list.html', {'usuarios': usuarios})

# Vista para crear un usuario
def usuario_create(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usuarios_list')
    else:
        form = UsuarioForm()
    return render(request, 'usuario_form.html', {'form': form})

# Vista para editar un usuario
def usuario_update(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('usuarios_list')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuario_form.html', {'form': form})

# Vista para eliminar un usuario
def usuario_delete(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('usuarios_list')
    return render(request, 'usuario_confirm_delete.html', {'usuario': usuario})
