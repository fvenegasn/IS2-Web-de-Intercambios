from django.contrib import admin
from django.urls import path, include

from intercambios_caritas import views

urlpatterns = [
    path('', views.home, name="home"),  # www.hola.com/
    # www.hola.com/register/
    path('register', views.register, name="register"),
    path('login', views.signin, name="signin"),  # www.hola.com/login
    path('logout', views.signout, name="signout"),  # www.hola.com/logout
    path('quienes_somos', views.quienes_somos, name="quienes_somos"),
]
