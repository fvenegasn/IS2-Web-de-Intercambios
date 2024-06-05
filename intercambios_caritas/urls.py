from django.contrib import admin
from django.urls import path, include

from intercambios_caritas import views

from django.contrib.auth import views as auth_views

from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('', views.home, name="home"),  # www.hola.com/
    # www.hola.com/register/
    path('register', views.register, name="register"),
    path('login', views.signin, name="signin"),  # www.hola.com/login
    path('logout', views.signout, name="signout"),  # www.hola.com/logout
    path('quienes_somos', views.quienes_somos, name="quienes_somos"),
    
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='authentication\password_reset.html'),
         name="reset_password"), # resetear contraseña
    
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='authentication\password_reset_sent.html'),
         name="password_reset_done"), # envia el email de éxito para el reseteo de password
    
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='authentication\password_reset_form.html'), 
         name="password_reset_confirm"), # link al password reset form desde el mail
    
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='authentication\password_reset_done.html'), 
         name="password_reset_complete"), # contraseña cambiada exitosamente
    path('mi_pefil', views.mi_perfil ,name = "mi_perfil"),
    path('perfil/<str:username>/', views.ver_perfil, name='ver_perfil'),
    path('crear_publicacion', views.crear_publicacion,name="crear_publicacion"),
    path('mis_publicaciones', views.mis_publicaciones, name="mis_publicaciones"),
    path('ver_publicacion/<int:publicacion_id>/', views.ver_publicacion, name="ver_publicacion"),

    path('listar_usuarios', views.listar_usuarios, name="listar_usuarios"),
    path('crear_oferta/<int:publicacion_id>/', views.crear_oferta, name='crear_oferta'),
    path('ofertas_realizadas', views.ver_ofertas_realizadas, name='ver_ofertas_realizadas'),
    path('ofertas_recibidas', views.ver_ofertas_recibidas, name='ver_ofertas_recibidas'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
