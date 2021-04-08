from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import render

from tarjetas.models import Tarjeta
from tarjetas.serializers import TarjetaSerializer
from listas.models import Lista
from listas.serializers import ListaSerializer


# Create your views here.
class ListasViewSet(viewsets.ModelViewSet):
    serializer_class = ListaSerializer
    queryset = Lista.objects.all()
    permission_classes = [IsAuthenticated]

    @action(methods = ['POST'], detail = True)
    def cambiar_nombre(self, request, pk = None):
        lista = self.get_object()
        try:
            nombre = request.POST.get('nombre')
            lista.nombre = nombre
            lista.save()
            return Response("Change name list", status=status.HTTP_201_CREATED)
        except:
            return Response("Error to change name list ", status=status.HTTP_400_BAD_REQUEST)

    @action(methods = ['POST'], detail = True)
    def cambiar_posicion(self, request, pk = None):
        lista = self.get_object()
        try:
            posicion = request.POST.get('posicion')
            lista.posicion = posicion
            lista.save()
            return Response("Change list position", status=status.HTTP_201_CREATED)
        except:
            return Response("Error to change position", status=status.HTTP_400_BAD_REQUEST)

    @action(methods = ['POST'], detail = True)
    def agregar_tarjeta(self, request, pk = None):
        lista = self.get_object()
        tarjeta = {
            'nombre': request.POST.get('nombre'),
            'lista': lista.id,
            'descripcion': request.POST.get('descripcion'),
            'miembros': [request.POST.get('dueño')],
            'dueño': request.POST.get('dueño'),
            'fecha_vencimiento': request.POST.get('fecha_vencimiento'),
            'posicion': request.POST.get('posicion'),
        }
        serializer = TarjetaSerializer(data=tarjeta)
        if serializer.is_valid():
            serializer.save()
            return Response("Tarjeta created", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
