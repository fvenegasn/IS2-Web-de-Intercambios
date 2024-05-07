import datetime
import django
from django.http import HttpResponse
from django.shortcuts import redirect, render
from . import views
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

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
        if User.objects.filter(username=dni):
            messages.error(request, "El DNI ya está registrado")
            return redirect("register")
        
        if User.objects.filter(email=email):
            messages.error(request, "El email ya se encuentra registrado")            
            return redirect("register")
        
        if len(dni)>8 or len(dni)<8:
            messages.error(request, "El DNI debe contener 8 dígitos")
            return redirect("register")
        
        if len(password)<8:
            messages.error(request, "La contraseña debe tener, al menos, 8 caracteres")
            return redirect("register")

        # lo voy a poner mas lindo cuando tengamos un helpers.py
        now = datetime.datetime.now()
        nacimiento_parseado = datetime.datetime.strptime(nacimiento, "%Y-%m-%d")
        edad = now.year - nacimiento_parseado.year - ((now.month, now.day) < (nacimiento_parseado.month, nacimiento_parseado.day))

        if edad < 18:
            messages.error(request, "Debe ser mayor de 18 años para registrarse en este sitio")
            return redirect("register")

        
        # Si las validaciones estan OK (no entra en ningun if), crea usuario
        nuevo_usuario = User.objects.create_user(username=dni, email=email, password=password)
        nuevo_usuario.first_name = nombre
        nuevo_usuario.last_name = apellido
        #nuevo_usuario. = telefono
        #nuevo_usuario.direccion = direccion
        #nuevo_usuario.nacimiento = nacimiento

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
        usuario = authenticate(username=dni, password=password)

        # Si autentica OK
        if usuario is not None: # equivalente a null
            login(request, usuario)
            nombre = usuario.first_name # no anda
            return render(request, "authentication/index.html", {'fname': nombre})
        
        # Si no autentica OK
        else:
            messages.error(request, "El DNI o la contraseña ingresadas son incorrectas")
            # aca entiendo que tendríamos que llevar el conteo de intentos incorrectos
            #contador_incorrectos+=1
            #if (contador_incorrectos = 3 ):
            #    bloquear_cuenta()
            return redirect("signin")

    return render(request, "authentication/login.html")

def signout(request):
    logout(request)
    messages.success(request, "Cerraste tu sesión")
    return redirect("home")
