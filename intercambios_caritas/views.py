import datetime
import django
from django.http import HttpResponse
from django.shortcuts import redirect, render

from intercambios_caritas.models import Usuario
from . import views
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
#from is2.settings import LOGIN_ATTEMPTS_LIMIT

# Create your views here.


def home(request):
    return render(request, 'authentication/index.html')


def register(request):
    # Si mandaron el formulario
    if request.method == "POST":
        # Almaceno datos de usuario en variables
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        dni = request.POST['dni']
        telefono = request.POST['telefono']
        direccion = request.POST['direccion']
        nacimiento = request.POST['nacimiento']
        email = request.POST['mail']
        password = request.POST['password']

        # Evaluo condiciones de registro
        if Usuario.objects.filter(username=dni):
            return render(request, "authentication/register.html", {"error": "El DNI ya está registrado", "n": nombre, "a": apellido, "d": dni, "t": telefono, "dir": direccion, "nac": nacimiento, "e": email})

        if Usuario.objects.filter(email=email):
            return render(request, "authentication/register.html", {"error": "El email ya se encuentra registrado", "n": nombre, "a": apellido, "d": dni, "t": telefono, "dir": direccion, "nac": nacimiento, "e": email})

        if len(dni) > 8 or len(dni) < 8:
            return render(request, "authentication/register.html", {"error": "El DNI debe contener 8 dígitos", "n": nombre, "a": apellido, "d": dni, "t": telefono, "dir": direccion, "nac": nacimiento, "e": email})

        if len(password) < 8:
            return render(request, "authentication/register.html", {"error": "La contraseña debe tener, al menos, 8 caracteres", "n": nombre, "a": apellido, "d": dni, "t": telefono, "dir": direccion, "nac": nacimiento, "e": email})

        # lo voy a poner mas lindo cuando tengamos un helpers.py
        now = datetime.datetime.now()
        nacimiento_parseado = datetime.datetime.strptime(
            nacimiento, "%Y-%m-%d")
        edad = now.year - nacimiento_parseado.year - \
            ((now.month, now.day) < (nacimiento_parseado.month, nacimiento_parseado.day))

        if edad < 18:
            return render(request, "authentication/register.html", {"error": "Debe ser mayor de 18 años para registrarse en este sitio", "n": nombre, "a": apellido, "d": dni, "t": telefono, "dir": direccion, "nac": nacimiento, "e": email})

        # Si las validaciones estan OK (no entra en ningun if), crea usuario
        nuevo_usuario = Usuario.objects.create_user(
            username=dni, email=email, password=password)
        nuevo_usuario.first_name = nombre
        nuevo_usuario.last_name = apellido
        nuevo_usuario.telefono = telefono
        nuevo_usuario.direccion = direccion
        nuevo_usuario.nacimiento = nacimiento

        # OPCIONAL? -> activar usuario - min. 01.02.50

        nuevo_usuario.save()

        # OPCIONAL? -> mail de bienvenida - min. 00.53.06

        # Lleva al home
        messages.success(request, "Cuenta creada con éxito!")
        return redirect('home')

    return render(request, "authentication/register.html")


def signin(request):

    # Si mandaron el formulario
    if request.method == 'POST':
        # Almaceno datos de usuario en variables
        dni = request.POST['dni']
        password = request.POST['password']

        # Método para autenticar usuario?
        user = authenticate(username=dni, password=password)

        # Si autentica OK
        if user is not None:  # equivalente a null
            login(request, user)
            nombre = user.first_name  # update 07.05 -> no me preguntes cómo pero ahora anda
            return render(request, "authentication/index.html", {'aviso': f"Hola {nombre} has iniciado sesión"})

        # Si no autentica OK
        else:
            messages.error(
                request, "El DNI o la contraseña ingresadas son incorrectas")
            # Me fijo que exista como usuario
            user = Usuario.objects.filter(username=dni).first()
            # Si existe
            """if user is not None:
                user.login_attempts += 1
                user.save()
                if user.login_attempts >= LOGIN_ATTEMPTS_LIMIT:
                    user.is_active = False
                    user.save()
                    messages.error(
                        request, "Alcanzaste el máximo de intentos permitidos. Cuenta bloqueada")
        if user.is_active == False:
            messages.error(request, "Cuenta bloqueada")
        return redirect("signin")"""

    return render(request, "authentication/login.html")


def signout(request):
    logout(request)
    return render(request, "authentication/index.html", {'aviso': "Sesión cerrada exitosamente"})


def quienes_somos(request):
    return render(request, 'authentication/quienes_somos.html')
