from django.urls import path
from Usuario.API.views import *

urlpatterns = [
    path('crear/', crear_usuario, name='crear_usuario'),
    path('obtener/', obtener_usuarios, name='obtener_usuarios'),
    path('actualizar/<int:pk>/',modificar_usuario,name='modificar_usuario'),
    path('login/', LoginJWTView.as_view(), name='login_jwt'),
    path('logout/', LogoutJWTView.as_view(), name='logout_jwt'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
]