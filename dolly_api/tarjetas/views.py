from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from tarjetas.models import Tarjeta
from tarjetas.serializers import TarjetaSerializer


# Create your views here.
class TarjetasViewSet(viewsets.ModelViewSet):
    serializer_class = TarjetaSerializer
    queryset = Tarjeta.objects.all()
    permission_classes = [IsAuthenticated]