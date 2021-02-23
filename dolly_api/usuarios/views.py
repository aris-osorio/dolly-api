import base64
import uuid

from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response

from correos.enviar import Enviar
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render

from tableros.models import Tablero
from tableros.serializers import TableroSerializer
from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer, validar_pwd


# Create your views here.
class UsuariosViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    queryset = Usuario.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.is_valid():
            guardar = serializer.save()
            usuario = Usuario.objects.get(email=serializer.data["email"])
            token, _ = Token.objects.get_or_create(user=usuario)
            Enviar.confirmacion(serializer.data, token.key)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['POST'])
    def actualizar_password(self, request, pk=None):
        usuario = self.get_object()
        
        if(len(request.data['password']) <= 7):
            return Response("Password must have at least 8 characters", status=status.HTTP_400_BAD_REQUEST)

        try:
            validar = validar_pwd(request.data['password'])
        except:
            return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST) 
        
        if(validar == True):
            usuario.set_password(request.data['password'])
            usuario.save()
            usuario.auth_token.delete()
            return Response('Password set',status=status.HTTP_200_OK)

        return Response({'password': 
            'The password must include at least one: upper case letter, upper case letter, digit, special character'}, 
            status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods = ['GET'], detail = True)
    def mostrar_tableros(self, request, pk = None):
        tableros = Tablero.objects.filter(dueño = pk)
        serializer = TableroSerializer(tableros, many = True)
        return Response(status = status.HTTP_200_OK, data = serializer.data)

    @action(methods = ['GET'], detail = True)
    def tableros_favoritos(self, request, pk = None):
        tableros = Tablero.objects.filter(dueño = pk).filter(favorito = True)
        serializer = TableroSerializer(tableros, many = True)
        return Response(status = status.HTTP_200_OK, data = serializer.data)


@api_view(['POST'])
def login(request):
    try:
        email = request.POST.get('email')
        password = request.POST.get('password')
    except:
        return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)
    
    try:
        usuario = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return Response("Invalid email", status=status.HTTP_400_BAD_REQUEST)
    
    pwd_invalido = check_password(password, usuario.password)

    if not pwd_invalido:
        return Response("Invalid password", status=status.HTTP_400_BAD_REQUEST)
    
    if not usuario.is_active:
        return Response("email is not active", status=status.HTTP_400_BAD_REQUEST)
    
    token, _ = Token.objects.get_or_create(user=usuario)

    return Response(token.key, status=status.HTTP_200_OK)

@api_view(['POST'])
def logout(request):
    try:
        email = request.POST.get('email')
    except:
        return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)

    try:
        usuario = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return Response("Invalid email", status=status.HTTP_400_BAD_REQUEST)

    try:
        usuario.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist): 
        pass

    return Response("Successfully logged out.", status=status.HTTP_200_OK)

@api_view(['POST'])
def confirmacion(request):
    try:
        id = request.POST.get('id')
        token = request.POST.get('token')
    
        base64_bytes = id.encode('ascii')
        id_bytes = base64.b64decode(base64_bytes)
        id = id_bytes.decode('ascii')

        base64_bytes = token.encode('ascii')
        token_bytes = base64.b64decode(base64_bytes)
        token = token_bytes.decode('ascii')
    except:
        return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)

    try:
        usuario = Usuario.objects.get(id=id)
    except Usuario.DoesNotExist:
        return Response("Invalid user", status=status.HTTP_400_BAD_REQUEST)
    
    try:
        usuario_token = Token.objects.get(user=usuario)
    except: return Response("invalid token", status=status.HTTP_400_BAD_REQUEST)

    usuario.is_active = True
    usuario.save()
    
    try:
        usuario.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist): 
        pass
    
    return Response("Email successfully activated", status=status.HTTP_200_OK)

@api_view(['POST'])
def recuperar(request):
    try:
        email = request.POST.get('email')
    except:
        return Response("Invalid data", status=status.HTTP_400_BAD_REQUEST)
    
    try:
        usuario = Usuario.objects.get(email=email)
        token, _ = Token.objects.get_or_create(user=usuario)
        usuario = {
            'id': str(usuario.id),
            'first_name': usuario.first_name,
            'last_name': usuario.last_name,
            'email': usuario.email,
            'password': usuario.password,
            'is_active': usuario.is_active
        }
    except Usuario.DoesNotExist:
        return Response("Invalid email", status=status.HTTP_400_BAD_REQUEST)
    
    if not usuario['is_active']:
        return Response("Email is not active", status=status.HTTP_400_BAD_REQUEST)
    print(token.key)
    Enviar.recuperar(usuario, token.key)

    return Response("Email sent successfully", status=status.HTTP_200_OK)