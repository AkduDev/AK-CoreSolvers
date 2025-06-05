from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UsuarioSerializer
from Usuario.models import Usuario, SesionUsuario
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny


@api_view(['POST'])
def crear_usuario(request):
    if request.method == 'POST':
        serializer = UsuarioSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(
        {"error": "Método no permitido"},
        status=status.HTTP_405_METHOD_NOT_ALLOWED
    )


@api_view(['PUt','GET'])
def modificar_usuario(request,pk=None):
    usuario=Usuario.objects.filter(id=pk).first()

    if request.method=='PUT' and usuario:
        serializer=UsuarioSerializer(usuario,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='GET':
        serializer=UsuarioSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)



    

@api_view(['GET'])
def obtener_usuarios(request):

    if request.method=='GET':        
        try:
            usuarios = Usuario.objects.all()
            serializer = UsuarioSerializer(usuarios, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 
    return "Error no es un metodo Get"


class LoginJWTView(APIView):
    permission_classes = [AllowAny] 
    authentication_classes = []
    
    def post(self, request):
        correo = request.data.get('correo')
        password = request.data.get('password')

        if not correo or not password:
            return Response({'error': 'Correo y contraseña son obligatorios'}, status=status.HTTP_400_BAD_REQUEST)

        usuario = authenticate(username=correo, password=password)

        if not usuario:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

        if not usuario.is_active:
            return Response({'error': 'El usuario no está activo'}, status=status.HTTP_403_FORBIDDEN)

    
        refresh = RefreshToken.for_user(usuario)
        access_token = str(refresh.access_token)

        try:
            sesion = SesionUsuario.objects.create(
                usuario=usuario,
                token=access_token,  # Puedes guardar solo el hash si prefieres
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                activa=True
            )
        except Exception as e:
            return Response({'error': 'No se pudo registrar la sesión'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'access': access_token,
            'refresh': str(refresh),
            'mensaje': 'Inicio de sesión exitoso',
            'sesion_id': sesion.id
        }, status=status.HTTP_200_OK)
    

class LogoutJWTView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"error": "Se requiere el campo 'refresh' en el cuerpo de la solicitud"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            
            token = RefreshToken(refresh_token)

            
            token.blacklist()

            
            request.user.sesionusuario_set.update(activa=False)

            return Response(
                {"mensaje": "Cierre de sesión exitoso. Token añadido a la lista negra."},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {"error": f"No se pudo cerrar sesión: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
    

class PerfilView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'mensaje': f'Bienvenido {request.user.nombre} {request.user.apellido}',
            'correo': request.user.correo,
            'telefono': request.user.telefono
        })