import datetime
import django
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from intercambios_caritas.forms import IntercambioForm, PublicacionForm
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
            messages.warning(request, "El DNI ya está registrado.")
            return render(request, "authentication/register.html", {"n": nombre, "a": apellido, "d": dni, "t": telefono, "dir": direccion, "nac": nacimiento, "e": email})

        if Usuario.objects.filter(email=email):
            messages.warning(request, "El email ya se encuentra registrado.")
            return render(request, "authentication/register.html", {"n": nombre, "a": apellido, "d": dni, "t": telefono, "dir": direccion, "nac": nacimiento, "e": email})

        if len(dni) > 8 or len(dni) < 8:
            messages.warning(request, "El DNI debe contener 8 dígitos.")
            return render(request, "authentication/register.html", {"n": nombre, "a": apellido, "d": dni, "t": telefono, "dir": direccion, "nac": nacimiento, "e": email})

        if len(password) < 8:
            messages.warning(
                request, "La contraseña debe tener, al menos, 8 caracteres.")
            return render(request, "authentication/register.html", {"n": nombre, "a": apellido, "d": dni, "t": telefono, "dir": direccion, "nac": nacimiento, "e": email})

        # lo voy a poner mas lindo cuando tengamos un helpers.py
        now = datetime.datetime.now()
        nacimiento_parseado = datetime.datetime.strptime(
            nacimiento, "%Y-%m-%d")
        edad = now.year - nacimiento_parseado.year - \
            ((now.month, now.day) < (nacimiento_parseado.month, nacimiento_parseado.day))

        if edad < 18:
            messages.warning(
                request, "Debe ser mayor de 18 años para registrarse.")
            return render(request, "authentication/register.html", {"n": nombre, "a": apellido, "d": dni, "t": telefono, "dir": direccion, "nac": nacimiento, "e": email})

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
            publicacion = form.save(commit=False)
            publicacion.usuario = request.user
            inicio = form.cleaned_data.get('franja_horaria_inicio')
            fin = form.cleaned_data.get('franja_horaria_fin')
            if inicio and fin:
                publicacion.franja_horaria = f"entre las {inicio.strftime('%H:%M')} y las {fin.strftime('%H:%M')}"
            publicacion.save()
            print (publicacion)
            messages.success(request, "Publicación creada exitosamente!")
            return redirect('home')
        else:
            messages.warning(request, "Error, Publicación no creada.")
    return render(request, 'publicacion/crear_publicacion.html', {'form': form})


def mis_publicaciones(request):
    usuario_actual = request.user.username
    publicaciones = Publicacion.objects.filter(usuario_dni=usuario_actual)
    # si le pasas index anda
    return render(request, 'publicacion/mis_publicaciones.html', {'publicaciones': publicaciones})


def ver_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, pk=publicacion_id)
    return render(request, 'publicacion/ver_publicacion.html', {'publicacion': publicacion})


def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    # si le pasas index anda
    return render(request, 'administracion_usuarios/listar_usuarios.html', {'usuarios': usuarios})

def crear_oferta(request, publicacion_id):
    publicacion_demandada = Publicacion.objects.get(id=publicacion_id)

    if request.method == "POST":
        form = IntercambioForm(request.POST, user=request.user)
        if form.is_valid():
            propuesta = form.save(commit=False)
            propuesta.publicacion_demandada = publicacion_demandada
            propuesta.publicacion_ofertante = Publicacion.objects.get(id=form.cleaned_data['publicacion_ofertante'])
            if propuesta.es_valida():
                propuesta.save()
                messages.success(request, "Propuesta de intercambio creada exitosamente.")
                return redirect('home')
            else:
                messages.error(request, "Propuesta de intercambio inválida.")
    else:
        form = IntercambioForm(user=request.user)

    context = {
        'form': form,
        'publicacion_demandada': publicacion_demandada
    }
    return render(request, 'publicacion/crear_oferta.html', context)