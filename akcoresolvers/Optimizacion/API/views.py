from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from Optimizacion.API.servicios import *

class ResolverGraficoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        datos = request.data
        resultado = resolver_grafico(datos)
        return Response(resultado)


class MostrarGraficoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        datos = request.data
        buf = generar_grafico(datos)

        if isinstance(buf, dict) and 'error' in buf:
            return Response(buf, status=400)

        return HttpResponse(buf.getvalue(), content_type="image/png")