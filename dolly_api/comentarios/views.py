from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render
from rest_framework import viewsets
from comentarios.models import Comentario
from comentarios.serializers import ComentarioSerializer


# Create your views here.
class ComentariosViewSet(viewsets.ModelViewSet):
    serializer_class = ComentarioSerializer
    queryset = Comentario.objects.all()
    permission_classes = [IsAuthenticated]