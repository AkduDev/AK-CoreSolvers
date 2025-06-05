from Usuario.models import SesionUsuario
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication

class RegistroActividadJWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jwt_auth = JWTAuthentication()
        header = jwt_auth.get_header(request)
        if header:
            raw_token = jwt_auth.get_raw_token(header)
            if raw_token:
                validated_token = jwt_auth.get_validated_token(raw_token)
                user = jwt_auth.get_user(validated_token)
                if user.is_authenticated:
                    try:
                        # Actualiza la última actividad de la sesión activa
                        SesionUsuario.objects.filter(usuario=user, activa=True).update(
                            ultima_actividad=timezone.now()
                        )
                    except Exception as e:
                        print(f"Error actualizando última actividad: {e}")

        return self.get_response(request)