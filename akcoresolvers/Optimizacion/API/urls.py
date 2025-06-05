from django.urls import path
from .views import *

urlpatterns = [
    path('grafico/', ResolverGraficoView.as_view(), name='resolver_grafico'),
    path('graficomostrar/', MostrarGraficoView.as_view(), name='mostrar_grafico'),
]