"""
URL configuration for aeropuertoInternacional project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from vueloApp import views

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.iniciar_sesion, name='login'),
    path('registrarse', views.registrarse, name='registrarse'),
    path('inicio', views.inicio, name='inicio'),
    path('destino', views.destinos, name='destinos'),
    path('aerolineas', views.aerolineas, name='aerolineas'),
    path('aerolineas/<int:id>/', views.detalle_aerolinea, name='detalle_aerolinea'),
    path('contacto', views.contacto, name='contacto'),
    path('crear_boleto', views.crear_boleto, name='crear_boleto'),
    path('vista_boletos', views.vista_boletos, name='vista_boletos'),
    path('editar_boleto/<int:boleto_id>', views.editar_boleto, name='editar_boleto'),
    path('eliminar_boleto/<int:boleto_id>', views.eliminar_boleto, name='eliminar_boleto'),
    
]
