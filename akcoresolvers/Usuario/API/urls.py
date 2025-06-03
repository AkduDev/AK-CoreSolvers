from django.urls import path

from Usuario.API.views import crear_usuario, obtener_usuarios

urlpatterns = [
    path('crear/', crear_usuario, name='crear_usuario'),
    path('obtener/', obtener_usuarios, name='obtener_usuarios'),
]