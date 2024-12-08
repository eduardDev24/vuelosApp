from django import forms

from packApp2.models import Pack_promocion
from .models import Boleto, Contacto, Aerolinea
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Este correo electrónico ya está en uso.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        # Esto verifica si el nombre de usuario ya está en uso
        if User.objects.filter(username=cleaned_data.get('username')).exists():
            raise forms.ValidationError("El nombre de usuario ya está en uso.")

        return cleaned_data


class BoletoForm(forms.ModelForm):
    class Meta:
        model = Boleto
        fields = ['nombre', 'rut', 'destino_ida', 'destino_vuelta',
                  'asiento', 'horario', 'aerolinea', 'total_viaje', 'pack']

    aerolinea = forms.ModelChoiceField(
        queryset=Aerolinea.objects.all(), empty_label="Selecciona una aerolínea")
    pack = forms.ModelChoiceField(queryset=Pack_promocion.objects.all(
    ), required=False, empty_label="Selecciona un Pack")

    # Método para calcular el total según el número de boletos
    def clean_total_viaje(self):
        total_viaje = self.cleaned_data.get('total_viaje')
        return total_viaje or 0.0

    def clean(self):
        cleaned_data = super().clean()
        destino_ida = cleaned_data.get("destino_ida")
        destino_vuelta = cleaned_data.get("destino_vuelta")

        if destino_ida == destino_vuelta:
            raise forms.ValidationError(
                "El destino de ida y de vuelta no pueden ser el mismo.")

        return cleaned_data


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control'}),
        }
