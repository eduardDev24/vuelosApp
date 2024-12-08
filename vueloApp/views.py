
import requests
from django.shortcuts import render, redirect, get_object_or_404

from packApp2.models import Pack_promocion
from .models import Boleto, Aerolinea, Pais, Asiento, Horario
from .forms import BoletoForm, RegistroForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import ContactoForm
from django.utils import timezone

from django.shortcuts import render


@login_required(login_url='login')
def inicio(request):
    return render(request, 'inicio.html')


@login_required(login_url='login')
def destinos(request):
    return render(request, 'destinos.html')


@login_required(login_url='login')
def aerolineas(request):
    # Recupera todas las aerolíneas de la base de datos
    aerolineas = Aerolinea.objects.all()
    return render(request, 'aerolineas.html', {'aerolineas': aerolineas})


@login_required(login_url='login')
def detalle_aerolinea(request, id):
    aerolinea = get_object_or_404(Aerolinea, id=id)
    return render(request, 'detalle_aerolinea.html', {'aerolinea': aerolinea})


@login_required(login_url='login')
def contacto(request):
    return render(request, 'contacto.html')


@login_required(login_url='login')
def crear_boleto(request):
    if request.method == 'POST':
        form = BoletoForm(request.POST)
        if form.is_valid():
            boleto = form.save(commit=False)
            boleto.usuario = request.user  # Asociamos el usuario actual

            # Obtenemos el asiento y calcular el total
            asiento = Asiento.objects.get(id=form.cleaned_data['asiento'].id)
            boleto.total_viaje = asiento.precio

            # Obtenemos el pack seleccionado (si existe)
            # Esto es el pack seleccionado
            pack = form.cleaned_data.get('pack')
            if pack:
                boleto.pack = pack  # Asociamos el pack al boleto

            # Marcamos el asiento como no disponible
            if asiento.disponible:
                asiento.disponible = False
                asiento.save()

                boleto.save()
                messages.success(request, "Boleto creado exitosamente.")
                # Redirigimos después de guardar
                return redirect('crear_boleto')
            else:
                messages.error(request, "El asiento no está disponible.")
    else:
        form = BoletoForm()

    paises = Pais.objects.all()
    aerolineas = Aerolinea.objects.all()
    asientos = Asiento.objects.filter(disponible=True)
    horarios = Horario.objects.all()
    promociones = Pack_promocion.objects.all()

    return render(request, 'crear_boleto.html', {
        'form': form,
        'paises': paises,
        'aerolineas': aerolineas,
        'asientos': asientos,
        'horarios': horarios,
        'promociones': promociones,
    })


@login_required(login_url='login')
def vista_boletos(request):
    # Obtenemos los boletos creados por el usuario que inició sesión.
    boletos = Boleto.objects.filter(usuario=request.user)
    return render(request, 'vista_boletos.html', {'boletos': boletos})


@login_required
def editar_boleto(request, boleto_id):
    boleto = get_object_or_404(Boleto, id=boleto_id)
    if request.method == 'POST':
        form = BoletoForm(request.POST, instance=boleto)
        if form.is_valid():
            boleto = form.save(commit=False)

            # Obtenemos el pack seleccionado (si existe)
            pack = form.cleaned_data.get('pack')
            print(f"Pack seleccionado: {pack}")
            if pack:
                boleto.pack = pack  # Asociamos el pack al boleto
            else:
                boleto.pack = None  # Desasociamos el pack si no se selecciona ninguno

            boleto.save()
            messages.success(request, 'Boleto editado exitosamente.')
            return redirect('vista_boletos')
        else:
            messages.error(
                request, 'Error al editar el boleto. Por favor verifica los datos.')

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

            # Asignar privilegios a los usuarios con nombres especiales
            if user.username.lower() in ['administrador']:
                user.is_staff = True
                user.is_superuser = True  # Opcional: también lo puedes hacer superusuario
                user.save()

                # Redirigir al panel de administración
                return redirect('/admin/')

            # Mensaje de éxito para usuarios regulares
            messages.success(
                request, "Registro exitoso. Por favor, inicia sesión.")
            return redirect('login')
        else:
            # Mensaje de error si el formulario no es válido
            messages.error(
                request, "Error en el formulario. Revisa los datos ingresados.")
    else:
        form = RegistroForm()

    # Renderiza el formulario de registro
    return render(request, 'registrarse.html', {'form': form})


def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Intento de inicio de sesión: Username={
              username}, Password={password}")  # Depuración por consola

        # Autenticación del usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print(f"autenticación para el usuario: {username}")
            # Si el usuario es autenticado, iniciar sesión
            login(request, user)

            # Redirigir según los privilegios del usuario
            if user.is_staff or user.username.lower() in ['administrador']:
                return redirect('/admin/login/')
            else:
                # Redirige a la página principal para usuarios regulares
                return redirect('inicio')
        else:
            # Si las credenciales son incorrectas
            messages.error(request, "Usuario o contraseña no válidos.")
            # regresa al formulario de login
            return redirect('login')

    # Renderiza el formulario de inicio de sesión si el método es GET o si hay errores
    return render(request, 'login.html')


@login_required(login_url='login')
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


@login_required(login_url='login')
def destinos(request):
    api_key = '0268e0ced0b01895601ac7895cb4bbe7'
    endpoint = 'http://api.aviationstack.com/v1/flights'
    params = {
        'access_key': api_key,
        'arr_icao': 'SCEL',  # Código ICAO de Santiago de Chile (SCEL)
        'flight_status': 'active',  # Puede ser 'scheduled', 'active', etc.
    }

    try:
        # Usamos la biblioteca requests para realizar la solicitud al API
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Lanza una excepción si la respuesta no es exitosa
        # Asegura que se obtenga 'data' o una lista vacía
        vuelos = response.json().get('data', [])
    except requests.RequestException as e:
        print(f"Error al solicitar los datos: {e}")
        vuelos = []  # En caso de error, asigna una lista vacía

    return render(request, 'destinos.html', {'vuelos': vuelos})
