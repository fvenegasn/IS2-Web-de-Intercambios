import datetime
import django
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from intercambios_caritas.forms import PublicacionForm
from intercambios_caritas.models import Usuario, Publicacion
from . import views
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# from is2.settings import LOGIN_ATTEMPTS_LIMIT

# Create your views here.


def home(request):
    publicaciones = Publicacion.objects.all()
    return render(request, 'authentication/index.html', {'publicaciones': publicaciones})


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
        """ redirecciono al login, no al home """

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
            messages.success(request, "Sesión iniciada exitosamente!")
            return redirect('home')
        # Si no autentica OK
        else:
            messages.warning(request, "Usuario o contraseña incorrectos!")
            return render(request, "authentication/login.html", {"d": dni})

    return render(request, "authentication/login.html")


def signout(request):
    logout(request)
    messages.warning(request, "Sesión cerrada exitosamente!")
    return redirect('home')
    """ con redirect muestra las publicaciones, con render(request, "authentication/index.html") parece que no y con return home(request) el url no cambia queda /logout"""


def quienes_somos(request):
    return render(request, 'authentication/quienes_somos.html')


def ver_perfil(request):
    return render(request, 'administracion_usuarios/mi_perfil.html')


def crear_publicacion(request):
    form = PublicacionForm()
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save()
            publicacion.usuario_dni = request.user.username
            publicacion.usuario_nombre = request.user.first_name
            publicacion.save()
            messages.success(request, "Publicación creada con éxito!")
            return redirect('home')
        else:
            messages.error(request, "Publicación no creada")
    return render(request, 'publicacion/crear_publicacion.html', {'form': form})


def mis_publicaciones(request):
    usuario_actual = request.user.username
    publicaciones = Publicacion.objects.filter(usuario_dni=usuario_actual)
    # si le pasas index anda
    return render(request, 'publicacion/mis_publicaciones.html', {'publicaciones': publicaciones})


def ver_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, pk=publicacion_id)
    return render(request, 'publicacion/ver_publicacion.html', {'publicacion': publicacion})
