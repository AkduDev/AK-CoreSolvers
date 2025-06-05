from datetime import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from Usuario.models import SesionUsuario
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication



def iniciar_sesion(correo, password, request):
    usuario = authenticate(username=correo, password=password)
    if not usuario:
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

    if not usuario.is_active:
        return Response({'error': 'El usuario no está activo'}, status=status.HTTP_403_FORBIDDEN)

    refresh = RefreshToken.for_user(usuario)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    try:
        sesion = SesionUsuario.objects.create(
            usuario=usuario,
            token=access_token,
            refresh_token=refresh_token,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
        )
    except Exception as e:
        return Response({'error': 'No se pudo registrar la sesión'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({
        'access': access_token,
        'refresh': refresh_token,
        'mensaje': 'Inicio de sesión exitoso',
        'sesion_id': sesion.id
    }, status=status.HTTP_200_OK)


def cerrar_sesion(refresh_token, request):
    if not refresh_token:
        return Response({"error": "Se requiere el refresh token"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()

        SesionUsuario.objects.filter(usuario=request.user).update(activa=False)

        return Response({"mensaje": "Logout exitoso"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": "No se pudo cerrar sesión"}, status=status.HTTP_400_BAD_REQUEST)


def actualizar_actividad(usuario):
    
    SesionUsuario.objects.filter(usuario=usuario, activa=True).update(
    ultima_actividad=timezone.now())