from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from Optimizacion.API.servicios import *

#WOLFRAMMMMMMMMMMMMMMMMMMMMMMMM
from Optimizacion.API.MetodosWolfram import *
from Optimizacion.API.Wolfram_Alpha import *
from Optimizacion.API.MetodosWolfram.analisis_distribuciones import resolver_distribucion_wolfram_alpha
from Optimizacion.API.MetodosWolfram.probabilidades import resolver_probabilidad_wolfram_alpha
from Optimizacion.API.MetodosWolfram.simulaciones import resolver_simulacion_wolfram_alpha

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





class ChatMathView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        mensaje = request.data.get("mensaje")
        if not mensaje:
            return Response({"error": "Falta el campo 'mensaje'"})

        resultado = procesar_entrada(mensaje)
        return Response(resultado)


class ResolverSimplexView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        datos = request.data
        resultado = resolver_simplex(datos)

        # Debugging: Imprimir el resultado recibido
        print("Resultado en ResolverSimplexView:", resultado)

        if 'error' in resultado:
            return Response(resultado, status=400)

        return Response(resultado)

class ResolverDualSimplexView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        datos = request.data
        resultado = resolver_dual_simplex(datos)

        # Debugging: Imprimir el resultado recibido
        print("Resultado en ResolverDualSimplexView:", resultado)

        if 'error' in resultado:
            return Response(resultado, status=400)

        return Response(resultado)


class ResolverProbabilidadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        mensaje = request.data.get("mensaje")
        if not mensaje:
            return Response({"error": "Falta el campo 'mensaje'"})

        resultado = resolver_probabilidad_wolfram_alpha(mensaje)
        return Response(resultado)

class ResolverSimulacionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        mensaje = request.data.get("mensaje")
        if not mensaje:
            return Response({"error": "Falta el campo 'mensaje'"})

        resultado = resolver_simulacion_wolfram_alpha(mensaje)
        return Response(resultado)

class ResolverDistribucionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        mensaje = request.data.get("mensaje")
        if not mensaje:
            return Response({"error": "Falta el campo 'mensaje'"})

        resultado = resolver_distribucion_wolfram_alpha(mensaje)
        return Response(resultado)