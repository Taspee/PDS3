
from django import forms
from .models import Usuario, Casillero

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario

        fields = ['name', 'email']

class CasilleroPasswordForm(forms.ModelForm):
    class Meta:
        model = Casillero
        fields = ['password']  # Solo el campo de la contraseña
        widgets = {
            'password': forms.PasswordInput()  # Para mostrar el campo como un input de tipo password
        }