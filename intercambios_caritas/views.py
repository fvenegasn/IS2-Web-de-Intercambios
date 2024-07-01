import datetime
import django
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from intercambios_caritas.forms import IntercambioForm, PublicacionForm, UpdatePublicacionForm,PreguntaForm,RespuestaForm, FilialForm, FiltroIntercambiosForm
from intercambios_caritas.models import Intercambio, Usuario, Publicacion, Categoria,Pregunta,Respuesta, Filial

from . import views
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# from is2.settings import LOGIN_ATTEMPTS_LIMIT
from django.urls import reverse
from django.db.models import Q, ProtectedError
from django.db.models import BooleanField, ExpressionWrapper, F
import datetime
import json
from django.http import JsonResponse
from collections import Counter
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth,TruncDay
from django.utils import timezone

# Create your views here.


def home(request):
    queryset = request.GET.get('buscar')
    categorias_seleccionadas = request.POST.getlist('categoria') if 'categoria' in request.POST else []
    puntos_de_encuentro_seleccionados = request.POST.getlist('punto_encuentro') if 'punto_encuentro' in request.POST else []
    estados_seleccionados = request.POST.getlist('estado') if 'estado' in request.POST else []
    
    publicaciones_disponibles = Publicacion.objects.filter(
        disponible_para_intercambio=True, 
        usuario__is_active=True
    )

    if categorias_seleccionadas:
        publicaciones_disponibles = publicaciones_disponibles.filter(categoria__in=categorias_seleccionadas)

    if puntos_de_encuentro_seleccionados:
        filtered_publicaciones = Publicacion.objects.none()
        for punto in puntos_de_encuentro_seleccionados:
            filtered_publicaciones |= publicaciones_disponibles.filter(punto_encuentro__contains=punto)
        publicaciones_disponibles = filtered_publicaciones
        
    if estados_seleccionados:
        publicaciones_disponibles = publicaciones_disponibles.filter(estado__in=estados_seleccionados)
    if queryset:
        publicaciones_disponibles = publicaciones_disponibles.filter(
            Q(nombre__icontains=queryset) | 
            Q(categoria__icontains=queryset)
        ).distinct()

        

    return render(request, 'authentication/index.html', {
        'publicaciones': publicaciones_disponibles,
        'categorias': Publicacion.CATEGORIAS,
        'puntos_de_encuentro': Publicacion.PUNTOS_ENC,
        'estados': Publicacion.ESTADOS,
        'categorias_seleccionadas': categorias_seleccionadas,
        'puntos_de_encuentro_seleccionados': puntos_de_encuentro_seleccionados,
        'estados_seleccionados': estados_seleccionados,
        'queryset': queryset
    })



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

@login_required
def mi_perfil(request):
    return render(request, 'administracion_usuarios/mi_perfil.html')

from django.shortcuts import render, redirect
from .forms import CategoriaForm, UserUpdateForm

@login_required
def mi_perfil_modificar(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos actualizados exitosamente.')
            return redirect('mi_perfil')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'administracion_usuarios/mi_perfil_modificar.html', {'form': form})

@login_required
def mi_perfil_eliminar(request):
    if request.method == 'POST':
        user = request.user
        # Comprobar si el usuario tiene intercambios con estado aceptado
        intercambios_aceptados = Intercambio.objects.filter(Q(publicacion_ofertante__usuario=user) & (Q(estado="ACEPTADA") ))|Intercambio.objects.filter(Q(publicacion_demandada__usuario=user) & (Q(estado="ACEPTADA")))
        if intercambios_aceptados:
            messages.warning(request, 'Tienes intercambios aceptados actualmente, debes resolver los mismos antes de eliminar la cuenta.')
            return redirect('mi_perfil_eliminar')
        
        # Cancelar todos los intercambios pendientes del usuario
        intercambios_pendientes = Intercambio.objects.filter(Q(publicacion_ofertante__usuario=user, estado='PENDIENTE') | Q(publicacion_demandada__usuario=user, estado='PENDIENTE'))
        for intercambio in intercambios_pendientes:
            intercambio.cancelar("Usuario Eliminado")
        # Establecer disponible_para_intercambio en False para todas las publicaciones del usuario
        Publicacion.objects.filter(usuario=user, disponible_para_intercambio=True).update(disponible_para_intercambio=False)
        # si se eliminaran las publicacionese intercambios en cascada, no serían necesarias esas ultimas 3 lineas
        logout(request) 
        user.delete()
        messages.success(request, 'Cuenta eliminada exitosamente.')
        return redirect('home')
    else:
        return render(request, 'administracion_usuarios/mi_perfil_eliminar.html')
    
@login_required
def ver_perfil(request, username):
    user = get_object_or_404(Usuario, username=username)
    return render(request, 'administracion_usuarios/perfil.html', {'user': user})

@login_required
def cambiar_rol(request, username=None):
    if request.method == 'POST':
        username = request.POST.get('username')
        role = request.POST.get('rol')
        try:
            user = Usuario.objects.get(username=username)
            site = request.POST.get('filial-selection', '')
            role_changed = False
            filial_changed = False
            intercambios_aceptados = False
            intercambios = Intercambio.objects.filter(Q(publicacion_ofertante__usuario=user) & (Q(estado="ACEPTADA") ))|Intercambio.objects.filter(Q(publicacion_demandada__usuario=user) & (Q(estado="ACEPTADA")))

            # acá chequeo los roles
            if role != 'Usuario' and len(intercambios)>0:
                intercambios_aceptados=True
            elif role != user.getRol():
                # Cancelar todos los intercambios pendientes del usuario
                intercambios_pendientes = Intercambio.objects.filter(Q(publicacion_ofertante__usuario=user, estado='PENDIENTE') | Q(publicacion_demandada__usuario=user, estado='PENDIENTE'))
                for intercambio in intercambios_pendientes:
                    intercambio.cancelar()
                # Establecer disponible_para_intercambio en False para todas las publicaciones del usuario
                Publicacion.objects.filter(usuario=user, disponible_para_intercambio=True).update(disponible_para_intercambio=False)
                user.modificarRol(role)
                role_changed = True
                if role == 'Moderador' and site:
                    user.filial = site
                else:
                    user.filial = ''
                user.save()
            elif role == 'Moderador' and site and user.filial != site:
                user.filial = site
                user.save()
                filial_changed = True
            if intercambios_aceptados:
                messages.warning(request, 'El usuario tiene intercambios pendientes, debe resolver los mismos antes de cambiar el rol')
            elif role_changed:
                messages.success(request, 'Rol asignado exitosamente')
            elif filial_changed:
                messages.success(request, 'Filial cambiada exitosamente')
            else:
                messages.warning(request, 'El usuario ya posee el rol seleccionado')
                
            return redirect(reverse('ver_perfil', kwargs={'username': username}))

        except Usuario.DoesNotExist:
            return HttpResponse("User does not exist.", status=404)

    filiales_choices = Usuario.Filiales.choices
    return render(request, 'perfil/cambiar_rol.html', {
        'user': None if username is None else user,
        'filiales_choices': filiales_choices,
    })


def toggle_user_status(request, username=None):
    if request.method == 'POST':
        username = request.POST.get('username')
        status = False if request.POST.get('activar_usuario')==None else True
        user = Usuario.objects.get(username=username)
        status_changed = user.is_active != status
        if status_changed:
            # cambia el estado
            user.is_active = status
            user.save()

            # cancela los intercambios pendientes

            Intercambios = Intercambio.objects.filter(Q(publicacion_ofertante__usuario=user) & (Q(estado="ACEPTADA") ))|Intercambio.objects.filter(Q(publicacion_demandada__usuario=user) & (Q(estado="ACEPTADA")))

            if len(Intercambios)>0:
                for i in Intercambios:
                        i.desestimar('Usuario Suspendido')
                        i.publicacion_ofertante.disponible_para_intercambio = True
                        i.publicacion_ofertante.save()
                        i.publicacion_demandada.disponible_para_intercambio = True
                        i.publicacion_demandada.save()

    return render(request, 'administracion_usuarios/perfil.html', {'user': user})

@login_required
def crear_publicacion(request):

    if len(Categoria.objects.all()) == 0:
        messages.error(request, "No se pueden publicar productos en este momento. Intente más tarde.")
        return redirect("home")

    form = PublicacionForm()
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        
        print(request.POST)

        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.usuario = request.user
            inicio = form.cleaned_data.get('franja_horaria_inicio')
            fin = form.cleaned_data.get('franja_horaria_fin')
            categoria = form.cleaned_data.get('categoria')
            filiales = form.cleaned_data.get("filial")
            if inicio and fin:
                publicacion.franja_horaria = f"entre las {inicio.strftime('%H:%M')} y las {fin.strftime('%H:%M')}"
                publicacion.franja_horaria_inicio = inicio
                publicacion.franja_horaria_fin = fin
            publicacion.categoria_nueva = categoria
            #publicacion.fil
            #publicacion.filial = filiales
            publicacion.save()
            form.save_m2m() #?
            messages.success(request, "Publicación creada exitosamente!")
            return redirect('home')
        else:
            print (form.errors)
            error_messages = {
                'punto_encuentro': 'No se especificó un punto de encuentro.',
                'dias_convenientes': 'No se especificó un dia conveniente.',
                'franja_horaria_inicio': 'La hora de fin no puede ser menor a la hora de inicio.',
                'categoria':'No se especificó la categoría',
                'categoria_nueva':"No se especificó la categoría"
            }
            generic_error_message = 'Error, Publicación no creada. verificar datos ingresados.'
            custom_error_found = False
            for field in form.errors:
                if field in error_messages:
                    messages.warning(request, f"Error, Publicación no creada. {error_messages[field]}")
                    custom_error_found = True
            if not custom_error_found:
                messages.warning(request, generic_error_message)
    return render(request, 'publicacion/crear_publicacion.html', {'form': form})

@login_required
def modificar_mi_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    selected_puntos_encuentro = publicacion.punto_encuentro
    selected_dias_disponibles = publicacion.dias_convenientes
    if request.method == 'POST':
        form = UpdatePublicacionForm(request.POST, instance=publicacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos actualizados exitosamente.')
            return redirect('ver_publicacion')
    else:
        form =UpdatePublicacionForm(instance=publicacion)
    
    # Render a form or other content in case of GET request
    context = {
        'publicacion': publicacion,
        'form':form,
        'selected_puntos_encuentro':selected_puntos_encuentro,
        'selected_dias_disponibles':selected_dias_disponibles,
    }
    return render(request, 'publicacion/modificar_mi_publicacion.html', context)

@login_required
def bajar_mi_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    
    if request.method == 'POST':
        intercambios = Intercambio.objects.filter(Q(publicacion_ofertante=publicacion) | Q(publicacion_demandada=publicacion))
        
        # Si la publicacion alguna vez tuvo un intercambio la doy de baja, si no la deleteo
        if intercambios: 
            # Comprobar si el la publicacion tiene intercambios con estado aceptado
            intercambios_aceptados = intercambios.filter(estado="ACEPTADA")
            if intercambios_aceptados:
                messages.warning(request, 'Tienes intercambios aceptados actualmente, debes resolver los mismos antes de eliminar la publicacion.')
                return redirect('bajar_mi_publicacion')
            # Cancelar todos los intercambios pendientes de la publicacion
            intercambios_pendientes = intercambios.filter(estado='PENDIENTE')
            for intercambio in intercambios_pendientes:
                intercambio.cancelar("Publicacion eliminada") #esto podria ser mas especifico
            publicacion.disponible_para_intercambio = False  
            publicacion.save()
            messages.success(request, 'Publicacion eliminada exitosamente.')
        else:
            publicacion.delete()
            messages.success(request, 'Publicacion eliminada exitosamente de la base de datos.')
        return redirect('mis_publicaciones')
    else:
        return render(request, 'publicacion/ver_publicacion_eliminar.html', {'publicacion': publicacion})

@login_required
def mis_publicaciones(request):
    usuario_actual = request.user
    publicaciones = Publicacion.objects.filter(usuario=usuario_actual, disponible_para_intercambio=True)
    return render(request, 'publicacion/mis_publicaciones.html', {'publicaciones': publicaciones})


def ver_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, pk=publicacion_id)
    preguntas = Pregunta.objects.filter(publicacion=publicacion)
    pregunta_form = PreguntaForm()
    respuesta_form = RespuestaForm()
    return render(request, 'publicacion/ver_publicacion.html', {'publicacion': publicacion,
                                                                'preguntas': preguntas,
                                                               'pregunta_form': pregunta_form,
                                                               'respuesta_form': respuesta_form})

@login_required
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    # si le pasas index anda
    return render(request, 'administracion_usuarios/listar_usuarios.html', {'usuarios': usuarios})

@login_required
def crear_oferta(request, publicacion_id):
    publicacion_demandada = Publicacion.objects.get(id=publicacion_id)

    usuario_actual = request.user
    publicaciones_del_usuario = Publicacion.objects.filter(usuario=usuario_actual, 
                                                           categoria=publicacion_demandada.categoria, 
                                                           disponible_para_intercambio=True)
    if len(publicaciones_del_usuario) == 0:
        messages.error(request,"Usted no posee publicaciones disponibles de esta categoría")
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
            filial_id = request.POST.get('filial')
            filial = Filial.objects.get(id=filial_id)
            propuesta.filial = filial
            print("LA ASIGNE")
            if propuesta.es_valida():
                
                propuesta.save()
                messages.success(request, "Propuesta de intercambio creada exitosamente.")
                return redirect('home')
            else:
                messages.error(request, "Propuesta de intercambio inválida.") # aca entra cuando no cumple con las RDN
        else:
            print (form.errors)
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

@login_required
def ver_ofertas_realizadas(request):
    ofertas_realizadas = Intercambio.objects.filter(publicacion_ofertante__usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'publicacion/ofertas_realizadas.html', {'ofertas_realizadas': ofertas_realizadas})

@login_required
def ver_ofertas_recibidas(request):
    ofertas_recibidas = Intercambio.objects.filter(publicacion_demandada__usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'publicacion/ofertas_recibidas.html', {'ofertas_recibidas': ofertas_recibidas})

@login_required
def ver_intercambios_moderador(request):
    filial_id = Filial.objects.get(nombre=request.user.filial)
    intercambios = Intercambio.objects.filter(
        Q(filial=filial_id) & 
        (Q(estado="ACEPTADA") | Q(estado="CONFIRMADA") | Q(estado="DESESTIMADA"))
    ).order_by('-fecha_creacion')
    
    if request.method == 'GET':
        form = FiltroIntercambiosForm(request.GET)
        if form.is_valid():
            usuario = form.cleaned_data.get('usuario')
            estado = form.cleaned_data.get('estado')
            fecha = form.cleaned_data.get('fecha')

            if usuario:
                intercambios = intercambios.filter(
                    Q(publicacion_ofertante__usuario=usuario) | Q(publicacion_demandada__usuario=usuario)
                )

            if estado and estado != 'Todos':
                intercambios = intercambios.filter(estado=estado)

            if fecha:
                intercambios = intercambios.filter(fecha_intercambio=fecha)
    else:
        form = FiltroIntercambiosForm()

    return render(request, 'publicacion/ver_intercambios.html', {'ofertas_recibidas': intercambios, 'form': form})

@login_required
def ver_mis_intercambios(request):
    ofertas_realizadas = Intercambio.objects.filter(
        Q(publicacion_ofertante__usuario=request.user) & 
        (Q(estado="ACEPTADA") | Q(estado="CONFIRMADA") | Q(estado="DESESTIMADA"))
    )
    ofertas_recibidas = Intercambio.objects.filter(
        Q(publicacion_demandada__usuario=request.user) & 
        (Q(estado="ACEPTADA") | Q(estado="CONFIRMADA") | Q(estado="DESESTIMADA"))
    )
    inter = ofertas_realizadas.union(ofertas_recibidas).order_by('-fecha_creacion')
    return render(request, 'publicacion/ver_intercambios.html', {'ofertas_recibidas': inter})

@login_required
def aceptar_oferta(request, oferta_id):
    oferta = get_object_or_404(Intercambio, id=oferta_id, publicacion_demandada__usuario=request.user)
    try:
        oferta.cancelar_ofertas_relacionadas()
        oferta.aceptar()

        oferta.publicacion_ofertante.disponible_para_intercambio = False
        oferta.publicacion_ofertante.save()
        oferta.publicacion_demandada.disponible_para_intercambio = False
        oferta.publicacion_demandada.save()
        messages.success(request, "Oferta aceptada exitosamente.")
    except ValueError as e:
        messages.error(request, str(e))
    return redirect('ver_ofertas_recibidas')

@login_required
def rechazar_oferta(request, oferta_id):
    oferta = get_object_or_404(Intercambio, id=oferta_id, publicacion_demandada__usuario=request.user)
    if request.method == 'POST':
        motivo = request.POST.get('motivo')
        motivo_otro = request.POST.get('motivo_otro')
        if motivo:
            if motivo == 'Otro'and not motivo_otro:
                messages.warning(request, "Debe indicar el motivo")
                return redirect('ver_ofertas_recibidas')
            elif motivo == 'Otro'and motivo_otro: 
                motivo = motivo_otro
            try:
                oferta.rechazar(motivo)
                messages.success(request, "Oferta rechazada exitosamente.")
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Debe seleccionar un motivo para rechazar la oferta.")
    return redirect('ver_ofertas_recibidas')

@login_required
def cancelar_oferta(request, oferta_id):
    oferta = get_object_or_404(Intercambio, id=oferta_id, publicacion_ofertante__usuario=request.user)
    if request.method == 'POST':
        motivo = request.POST.get('motivo')
        motivo_otro = request.POST.get('motivo_otro')
        if motivo:
            if motivo == 'Otro'and not motivo_otro:
                messages.warning(request, "Debe indicar el motivo")
                return redirect('ver_ofertas_realizadas')
            elif motivo == 'Otro'and motivo_otro: 
                motivo = motivo_otro
            try:
                oferta.cancelar(motivo)
                messages.success(request, "Oferta cancelada exitosamente.")
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Debe seleccionar un motivo para cancelar la oferta.")
    return redirect('ver_ofertas_realizadas')

def actualizar_calificaciones_y_donacion(oferta, request):
    # Actualizar calificaciones
    oferta.calificacion_demandante = request.POST.get('calificacion_demandada')
    oferta.calificacion_ofertante = request.POST.get('calificacion_ofertante')

    # Actualizar información de donación
    donacion_realizada = request.POST.get('donacion_realizada')
    if donacion_realizada == 'Si':
        oferta.hubo_donacion = True
        oferta.donacion_descripcion = request.POST.get('descripcion_donacion')
    else:
        oferta.hubo_donacion = False
        oferta.donacion_descripcion = "Sin descripción"  # O cualquier valor predeterminado

@login_required
def gestionar_intercambio(request, oferta_id):
    oferta = get_object_or_404(Intercambio, id=oferta_id)
    
    if request.method == 'POST':
        accion = request.POST.get('accion')

        if accion == 'confirmar_intercambio':
            try:
                actualizar_calificaciones_y_donacion(oferta, request)

                oferta.confirmar()
                oferta.save()
                messages.success(request, "Intercambio confirmado.")
            except ValueError as e:
                messages.warning(request, str(e))
                
        elif accion == 'desestimar_intercambio':
            motivo = request.POST.get('motivo')
            motivo_otro = request.POST.get('motivo_otro')
            if motivo:
                if motivo == 'Otro' and motivo_otro:
                    motivo = motivo_otro
                try:
                    actualizar_calificaciones_y_donacion(oferta, request)

                    oferta.desestimar(motivo)
                    oferta.publicacion_ofertante.disponible_para_intercambio = True
                    oferta.publicacion_ofertante.save()
                    oferta.publicacion_demandada.disponible_para_intercambio = True
                    oferta.publicacion_demandada.save()
                    oferta.save()  # No olvidar guardar después de desestimar
                    messages.success(request, "Intercambio desestimado.")
                except ValueError as e:
                    messages.warning(request, str(e))
            else:
                messages.warning(request, "Se requiere un motivo para desestimar el intercambio.")
    else:
        messages.warning(request, "Acción no permitida.")
    
    return redirect('ver_intercambios_moderador')


@login_required
def ver_metricas_filiales(request):
    # si le pasas index anda
    #Filiales = Filiales.objects.all() # esto despues hay que modificarlo para que filiales sea una clase por si sola
    return render(request, 'metricas/ver_metricas_filiales.html')

@login_required
def listar_categorias(request):
    # Me aseguro que sólo entren los admin
    user = request.user
    if user.rol != "Administrador":
        return redirect("home")

    if request.method == 'POST':
        if 'agregar_categoria' in request.POST:
            form = CategoriaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Categoría agregada exitosamente.")
                return redirect(reverse('listar_categorias'))
            else:
                messages.error(request, "La categoría ya existe.")
        elif 'eliminar_categoria' in request.POST:
            categoria_id = request.POST.get('categoria_id')
            categoria = Categoria.objects.get(id=categoria_id)
            try:
                categoria.delete()
                messages.success(request, "Categoría eliminada exitosamente.")
            except ProtectedError:
                messages.error(request, "No se puede eliminar la categoría hasta que no existan productos de la misma")
            return redirect(reverse('listar_categorias'))
    else:
        form = CategoriaForm()
    
    categorias = Categoria.objects.all()
    return render(request, 'publicacion/listar_categorias.html', {'categorias': categorias, 'form': form})

@login_required
def listar_filiales(request):
    # Me aseguro que sólo entren los admin
    user = request.user
    if user.rol != "Administrador":
        return redirect("home")

    if request.method == 'POST':
        if 'agregar_filial' in request.POST:
            form = FilialForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Filial agregada exitosamente.")
                return redirect(reverse('listar_filiales'))
            else:
                messages.error(request, "La filial ya existe.")
        elif 'eliminar_filial' in request.POST:
            filial_id = request.POST.get('filial_id')
            filial = Filial.objects.get(id=filial_id)
            try:
                filial.delete()
                messages.success(request, "Filial eliminada exitosamente.")
            except ProtectedError:
                messages.error(request, "No se puede eliminar la filial hasta que no existan intercambios en la misma")
            return redirect(reverse('listar_filiales'))
    else:
        form = FilialForm()

    filiales = Filial.objects.all()
    return render(request, 'publicacion/listar_filiales.html', {'filiales': filiales, 'form': form})

# Sección para visualizacion de metricas
# ------------------------------------------

def get_intercambios_mes(request):
    # Filter the queryset
    user = request.user
    if user.rol == "Moderador":
        intercambios = Intercambio.objects.filter(
            (Q(estado="ACEPTADA") | Q(estado="CONFIRMADA") | Q(estado="DESESTIMADA"))&Q(punto_encuentro = user.filial)
        ).annotate(year_month=TruncMonth('fecha_intercambio')).values('year_month', 'punto_encuentro').annotate(total=Count('id')).order_by('year_month')
    else:
        intercambios = Intercambio.objects.filter(
            Q(estado="ACEPTADA") | Q(estado="CONFIRMADA") | Q(estado="DESESTIMADA")
        ).annotate(year_month=TruncMonth('fecha_intercambio')).values('year_month', 'punto_encuentro').annotate(total=Count('id')).order_by('year_month')

    # Prepare the data for the chart
    finalrep = {}
    for item in intercambios:
        year_month = item['year_month'].strftime("%Y %B")
        punto_encuentro = item['punto_encuentro']
        total = item['total']
        
        if year_month not in finalrep:
            finalrep[year_month] = {}
        if punto_encuentro not in finalrep[year_month]:
            finalrep[year_month][punto_encuentro] = 0
        
        finalrep[year_month][punto_encuentro] += total

    return JsonResponse({'intercambios_mes': finalrep}, safe=False)




def get_intercambios_estado(request):
    # Filtra con los intercambios que me interesa mostrar
    user = request.user
    if user.rol =="Moderador":
        intercambios = Intercambio.objects.filter(Q(punto_encuentro = user.filial))
    else:
        intercambios = Intercambio.objects.all()

    # cuenta
    intercambios_counts = intercambios.values('estado').annotate(total=Count('id'))

    # Cinverte el resultado
    finalrep = {item['estado']: item['total'] for item in intercambios_counts}

    return JsonResponse({'intercambios_estado': finalrep}, safe=False)
@login_required
def agregar_pregunta(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    if request.user == publicacion.usuario:
        return redirect('ver_publicacion', publicacion_id=publicacion.id)  # O mostrar un mensaje de error
    if request.method == 'POST':
        form = PreguntaForm(request.POST)
        if form.is_valid():
            pregunta = form.save(commit=False)
            pregunta.publicacion = publicacion
            pregunta.usuario = request.user
            pregunta.save()
            return redirect('ver_publicacion', publicacion_id=publicacion.id)
    else:
        form = PreguntaForm()
    return render(request, 'publicacion/ver_publicacion.html', {'form': form, 'publicacion': publicacion})
@login_required
def agregar_respuesta(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, id=pregunta_id)
    if request.user != pregunta.publicacion.usuario:
        return redirect('ver_publicacion', publicacion_id=pregunta.publicacion.id)  # O mostrar un mensaje de error
    if request.method == 'POST':
        form = RespuestaForm(request.POST)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.pregunta = pregunta
            respuesta.usuario = request.user
            respuesta.save()
            return redirect('ver_publicacion', publicacion_id=pregunta.publicacion.id)
    else:
        form = RespuestaForm()
    return render(request, 'publicacion/ver_publicacion.html', {'form': form, 'pregunta': pregunta})

# ------------------------------------------


def get_intercambios_totales(request):
    user = request.user
    intercambios = None
    # Filter the queryset
    if user.rol == "Moderador":
        intercambios = Intercambio.objects.filter(
            (Q(estado="ACEPTADA") | Q(estado="CONFIRMADA") | Q(estado="DESESTIMADA"))&Q(punto_encuentro = user.filial)
        ).annotate(day=TruncDay('fecha_intercambio')).values('day').annotate(total=Count('id')).order_by('day')
        
    else:
        intercambios = Intercambio.objects.filter(
            Q(estado="ACEPTADA") | Q(estado="CONFIRMADA") | Q(estado="DESESTIMADA")
        ).annotate(day=TruncDay('fecha_intercambio')).values('day').annotate(total=Count('id')).order_by('day')

    finalrep = {}
    totalcum = 0
    for item in intercambios:
        day = item['day'].strftime("%Y-%m-%d")
        totalcum += item['total']
        finalrep[day] = totalcum

    return JsonResponse({'intercambios_dia_total': finalrep}, safe=False)

def mostrar_tabla_estadisticas(request):
    user = request.user
    if user.rol == "Moderador":
        intercambios = Intercambio.objects.filter(Q(punto_encuentro = user.filial))
    else:
        intercambios = Intercambio.objects.all()
    
    intercambios = list(intercambios.annotate(year_month=TruncMonth('fecha_intercambio')).values('year_month', 'punto_encuentro', 'estado').annotate(total=Count('id')).order_by('year_month'))
    return JsonResponse({'intercambios':intercambios}, safe=False)