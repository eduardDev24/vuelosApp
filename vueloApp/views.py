
from django.shortcuts import render, redirect, get_object_or_404
from .models import Boleto, Aerolinea, Pais, Asiento, Horario
from .forms import BoletoForm, RegistroForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ContactoForm
from django.utils import timezone


# Create your views here.
def inicio(request):
    return render(request, 'inicio.html')


def destinos(request):
    return render(request, 'destinos.html')


def aerolineas(request):
    # Recupera todas las aerolíneas de la base de datos
    aerolineas = Aerolinea.objects.all()
    return render(request, 'aerolineas.html', {'aerolineas': aerolineas})

#  Esta funcion queda para actualizar para mas adelante


def detalle_aerolinea(request, id):
    aerolinea = get_object_or_404(Aerolinea, id=id)
    return render(request, 'detalle_aerolinea.html', {'aerolinea': aerolinea})


def contacto(request):
    return render(request, 'contacto.html')


class CustomLoginView(LoginView):
    template_name = 'login.html'
    # Redirige a los usuarios autenticados automáticamente
    redirect_authenticated_user = True


def cerrar(request):
    if request.method == 'POST' and request.user.is_authenticated:
        messages.success(request, 'Has cerrado sesión exitosamente.')
    return render(request, 'login.html')


@login_required
def crear_boleto(request):
    if request.method == 'POST':
        form = BoletoForm(request.POST)
        if form.is_valid():
            boleto = form.save(commit=False)
            boleto.usuario = request.user

            # Obtenemos el asiento y calcular el total
            asiento = Asiento.objects.get(id=form.cleaned_data['asiento'].id)
            boleto.total_viaje = asiento.precio

            # Marcamos el asiento como no disponible
            if asiento.disponible:
                asiento.disponible = False
                asiento.save()

                boleto.save()
                messages.success(request, "Boleto creado exitosamente.")
                return redirect('crear_boleto')
            else:
                messages.error(request, "El asiento no está disponible.")
    else:
        form = BoletoForm()

    paises = Pais.objects.all()
    aerolineas = Aerolinea.objects.all()
    asientos = Asiento.objects.filter(disponible=True)
    horarios = Horario.objects.all()

    return render(request, 'crear_boleto.html', {
        'form': form,
        'paises': paises,
        'aerolineas': aerolineas,
        'asientos': asientos,
        'horarios': horarios,
    })


@login_required
def vista_boletos(request):
    boletos = Boleto.objects.all()
    return render(request, 'vista_boletos.html', {'boletos': boletos})


@login_required
def editar_boleto(request, boleto_id):
    boleto = get_object_or_404(Boleto, id=boleto_id)
    if request.method == 'POST':
        form = BoletoForm(request.POST, instance=boleto)
        if form.is_valid():
            form.save()

            return redirect('vista_boletos')
        else:
            # Mensaje de error
            messages.error(
                request, 'Error al editar el boleto. Por favor verifica los datos.')
            print(form.errors)  # Imprime los errores en la consola
    else:
        form = BoletoForm(instance=boleto)
    return render(request, 'editar_boleto.html', {'form': form, 'boleto': boleto})


@login_required
def eliminar_boleto(request, boleto_id):
    boleto = get_object_or_404(Boleto, id=boleto_id)
    if request.method == 'POST':
        boleto.delete()

        return redirect('vista_boletos')
    return render(request, 'eliminar_boleto.html', {'boleto': boleto})


def registrarse(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, "Registro exitoso. Por favor, inicia sesión.")
            # Redirige al login después del registro exitoso
            return redirect('login')
        else:
            messages.error(
                request, "Error en el formulario. Revisa los datos ingresados.")
    else:
        form = RegistroForm()
    return render(request, 'registrarse.html', {'form': form})


def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Autenticación del usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Si el usuario es autenticado, iniciar sesión
            login(request, user)
            # Redirige a la página de inicio si la autenticación es exitosa
            return redirect('inicio')
        else:
            # Si las credenciales son incorrectas, se muestra un mensaje de error
            messages.error(request, "Usuario o contraseña no válidos.")

    # Renderiza el formulario de inicio de sesión, incluso si el método es 'GET' o hay un error
    return render(request, 'login.html')


def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Guarda los datos en la base de datos
            form.save()
            # Muestra el mensaje de éxito
            messages.success(
                request, "Tu mensaje ha sido enviado exitosamente.")

            return redirect('contacto')
    else:
        form = ContactoForm()
    # implemento timestamp por problemas de carga del archivo css
    timestamp = timezone.now().timestamp()

    return render(request, 'contacto.html', {'form': form, 'timestamp': timestamp})
