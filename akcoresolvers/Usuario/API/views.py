from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UsuarioSerializer
from Usuario.models import Usuario


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