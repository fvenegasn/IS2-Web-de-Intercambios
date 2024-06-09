import datetime
import django
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from intercambios_caritas.forms import IntercambioForm, PublicacionForm
from intercambios_caritas.models import Intercambio, Usuario, Publicacion
from . import views
from django.contrib.auth.models import User
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# from is2.settings import LOGIN_ATTEMPTS_LIMIT
from django.urls import reverse

# Create your views here.


def home(request):
    publicaciones_disponibles = Publicacion.objects.filter(disponible_para_intercambio=True)
    return render(request, 'authentication/index.html', {'publicaciones': publicaciones_disponibles})




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
        nuevo_usuario.rol = 'Usuario' # creo que estoy duplicando con el init de la clase, pero nose si se invoca acá al constructor de la clase madre.

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


def mi_perfil(request):
    return render(request, 'administracion_usuarios/mi_perfil.html')

def ver_perfil(request, username):
    user = get_object_or_404(Usuario, username=username)
    return render(request, 'administracion_usuarios/perfil.html', {'user': user})

def cambiar_rol(request, username=None):
    user = None  # Assigning a default value to the user variable
    if request.method == 'POST':
        username = request.POST.get('username')
        role = request.POST.get('rol')
        
        try:
            user = Usuario.objects.get(username=username)
            site = request.POST.get('filial-selection', '')
            # Update the user's role
            if role != user.getRol:
                user.modificarRol(role)
                if role == 'Moderador' and site:
                    user.filial = site
                user.save()
            return redirect(reverse('ver_perfil', kwargs={'username': username}))
        except Usuario.DoesNotExist:
            return HttpResponse("User does not exist.", status=404)

    filiales_choices = Usuario.Filiales.choices
    return render(request, 'perfil/<str:username>/cambiar_rol/', {
        'user': user,
        'filiales_choices': filiales_choices,
        'messages': messages.get_messages(request),
    })


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
                publicacion.franja_horaria_inicio = inicio
                publicacion.franja_horaria_fin = fin
            publicacion.save()
            print (publicacion)
            messages.success(request, "Publicación creada exitosamente!")
            return redirect('home')
        else:
            messages.warning(request, "Error, Publicación no creada.")
    return render(request, 'publicacion/crear_publicacion.html', {'form': form})


def mis_publicaciones(request):
    usuario_actual = request.user
    publicaciones = Publicacion.objects.filter(usuario=usuario_actual)
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

    usuario_actual = request.user
    publicaciones_del_usuario = Publicacion.objects.filter(usuario=usuario_actual, categoria=publicacion_demandada.categoria)
    if len(publicaciones_del_usuario) == 0:
        messages.error(request,"Usted no posee publicaciones de esta categoría")
        return redirect("home")

    if request.method == "POST":
        print (request.POST)
        form = IntercambioForm(
            request.POST,
            user=usuario_actual,
            dias=publicacion_demandada.dias_convenientes,
            puntos=publicacion_demandada.punto_encuentro,
            categoria=publicacion_demandada.categoria,
            franja_horaria_inicio=publicacion_demandada.franja_horaria_inicio,
            franja_horaria_fin=publicacion_demandada.franja_horaria_fin
        )
        if form.is_valid():
            propuesta = form.save(commit=False)
            propuesta.publicacion_demandada = publicacion_demandada
            propuesta.publicacion_ofertante = form.cleaned_data['publicacion_ofertante']
            if propuesta.es_valida():
                propuesta.save()
                messages.success(request, "Propuesta de intercambio creada exitosamente.")
                return redirect('home')
            else:
                messages.error(request, "Propuesta de intercambio inválida.") # aca entra cuando no cumple con las RDN
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if error != "Este campo es obligatorio.":
                        messages.error(request, f"Error: {error}")
            #messages.error(request, "Verifique los datos ingresados.") # aca entra cuando directamente manda el formulario y hay algun dato mal
    else:
        form = IntercambioForm(
            user=usuario_actual,
            dias=publicacion_demandada.dias_convenientes,
            puntos=publicacion_demandada.punto_encuentro,
            categoria=publicacion_demandada.categoria,
            franja_horaria_inicio=publicacion_demandada.franja_horaria_inicio,
            franja_horaria_fin=publicacion_demandada.franja_horaria_fin
        )

    context = {
        'form': form,
        'publicacion_demandada': publicacion_demandada
    }
    return render(request, 'publicacion/crear_oferta.html', context)

def ver_ofertas_realizadas(request):
    ofertas_realizadas = Intercambio.objects.filter(publicacion_ofertante__usuario=request.user)
    return render(request, 'publicacion/ofertas_realizadas.html', {'ofertas_realizadas': ofertas_realizadas})

def ver_ofertas_recibidas(request):
    ofertas_recibidas = Intercambio.objects.filter(publicacion_demandada__usuario=request.user)
    return render(request, 'publicacion/ofertas_recibidas.html', {'ofertas_recibidas': ofertas_recibidas})

def aceptar_oferta(request, oferta_id):
    oferta = get_object_or_404(Intercambio, id=oferta_id, publicacion_demandada__usuario=request.user)
    try:
        oferta.aceptar()

        oferta.publicacion_ofertante.disponible_para_intercambio = False
        oferta.publicacion_ofertante.save()

        oferta.publicacion_demandada.disponible_para_intercambio = False
        oferta.publicacion_demandada.save()

        messages.success(request, "Oferta aceptada exitosamente.")
    except ValueError as e:
        messages.error(request, str(e))
    return redirect('ver_ofertas_recibidas')

def rechazar_oferta(request, oferta_id):
    oferta = get_object_or_404(Intercambio, id=oferta_id, publicacion_demandada__usuario=request.user)
    try:
        oferta.rechazar()
        messages.success(request, "Oferta rechazada exitosamente.")
    except ValueError as e:
        messages.error(request, str(e))
    return redirect('ver_ofertas_recibidas')

def cancelar_oferta(request, oferta_id):
    oferta = get_object_or_404(Intercambio, id=oferta_id, publicacion_ofertante__usuario=request.user)
    try:
        oferta.cancelar()
        messages.success(request, "Oferta cancelada exitosamente.")
    except ValueError as e:
        messages.error(request, str(e))
    return redirect('ver_ofertas_realizadas')