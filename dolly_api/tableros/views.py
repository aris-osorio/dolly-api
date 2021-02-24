from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from correos.enviar import Enviar
from django.shortcuts import render
from tableros.models import Tablero
from tableros.serializers import TableroSerializer
from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer


# Create your views here.
class TablerosViewSet(viewsets.ModelViewSet):
    serializer_class = TableroSerializer
    queryset = Tablero.objects.all()
    permission_classes = [IsAuthenticated]

    @action(methods = ['GET'], detail = True)
    def mostrar_dueño(self, request, pk = None):
        tablero = self.get_object()
        usuario = Usuario.objects.filter(id = tablero.dueño_id)
        serializer = UsuarioSerializer(usuario, many = True)
        return Response(status = status.HTTP_200_OK, data = serializer.data)

    @action(methods = ['GET'], detail = True)
    def mostrar_miembros(self, request, pk = None):
        tablero = self.get_object()
        serializer = UsuarioSerializer(tablero.miembros, many = True)
        return Response(status = status.HTTP_200_OK, data = serializer.data)
    
    @action(methods = ['POST'], detail = True)
    def agregar_miembro(self, request, pk = None):
        tablero = self.get_object()
        
        try:
            id = request.data['id']
            usuario = Usuario.objects.get(id=id)
            try:
                dueno = Usuario.objects.get(id=tablero.dueño_id).first_name
            except:
                return Response("Error agarrar usuario", status=status.HTTP_400_BAD_REQUEST)
            tablero.miembros.add(usuario)
            usuario = {
                'id': str(usuario.id),
                'first_name': usuario.first_name,
                'last_name': usuario.last_name,
                'email': usuario.email,
            }
            Enviar.invitacion(usuario, dueno, tablero.nombre)
        except:
            return Response("problem adding user to 'tablero'", status=status.HTTP_400_BAD_REQUEST)

        return Response("Adding user to 'tablero'", status=status.HTTP_200_OK)
    
    @action(methods = ['POST'], detail = True)
    def eliminar_miembro(self, request, pk = None):
        tablero = self.get_object()
        
        try:
            id = request.data['id']
            tablero.miembros.remove(Usuario.objects.get(id = id))
        except:
            return Response("problem removing user to 'tablero'", status=status.HTTP_400_BAD_REQUEST)

        return Response("Removing user to 'tablero'", status=status.HTTP_200_OK)
        
    @action(methods = ['POST'], detail = True)
    def cambiar_favorito(self, request, pk = None):
        tablero = self.get_object()
        favorito = request.POST.get('favorito')
        
        if((favorito == 'true') or (favorito == 'True') or (favorito ==  'TRUE')):
            tablero.favorito = True
        elif((favorito == 'false') or (favorito == 'False') or (favorito ==  'FALSE')):
            tablero.favorito = False
        else: 
            return Response("Invalid data (expected true or false)", status=status.HTTP_400_BAD_REQUEST)
        
        tablero.save()
        
        return Response("Favorite change successfully", status=status.HTTP_200_OK)
    
    @action(methods = ['POST'], detail = True)
    def cambiar_visibilidad(self, request, pk = None):
        tablero = self.get_object()
        visibilidad = request.POST.get('visibilidad')
        
        if((visibilidad == 'true') or (visibilidad == 'True') or (visibilidad ==  'TRUE')):
            tablero.visibilidad = True
        elif((visibilidad == 'false') or (visibilidad == 'False') or (visibilidad ==  'FALSE')):
            tablero.visibilidad = False
        else: 
            return Response("Invalid data (expected true or false)", status=status.HTTP_400_BAD_REQUEST)
        
        tablero.save()
        
        return Response("Visibility change successfully", status=status.HTTP_200_OK)