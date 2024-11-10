from django.shortcuts import render, get_object_or_404, redirect
from .models import Casillero, Usuario
from .email_operations import EmailOperations  # Importa la clase
from django.conf import settings  # Para obtener las credenciales desde settings.py
from .forms import CasilleroPasswordForm

# Vista para mostrar el estado de los casilleros
def casilleros_list(request):
    casilleros = Casillero.objects.select_related('usuario').all()  # Obtiene los casilleros con sus usuarios
    return render(request, 'casilleros_list.html', {'casilleros': casilleros})
def casillero_detail(request, casillero_id):
    casillero = get_object_or_404(Casillero, id=casillero_id)

    if request.method == 'POST':
        # Si se recibe el formulario para cambiar la contraseña
        form = CasilleroPasswordForm(request.POST, instance=casillero)
        if form.is_valid():
            form.save()  # Guarda la nueva contraseña
            return redirect('locker_detail', casillero_id=casillero.id)  # Redirige a la misma vista para ver los cambios
    else:
        form = CasilleroPasswordForm(instance=casillero)

    return render(request, 'casillero_detail.html', {'casillero': casillero, 'form': form})

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
# Vista para editar un usuario
def usuario_update(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()

            # Configuración del correo electrónico
            asunto = 'Tu contraseña ha sido cambiada'
            mensaje = f'Hola {usuario.name}, tu contraseña ha sido actualizada con éxito.'
            destinatarios = [usuario.email]  # Usa el email del usuario en la base de datos

            # Instancia de EmailOperations sin pasar username y password
            email_ops = EmailOperations()  # No necesitas pasar username ni password aquí
            
            # Enviar el correo
            email_ops.send_email(
                receivers_email=destinatarios,
                subject=asunto,
                message=mensaje
            )

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
