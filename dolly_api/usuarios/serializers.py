from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError 

import re
from usuarios.models import Usuario

def validar_pwd(pwd):
    digito = False
    especial = False
    mayuscula = False
    especiales = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        
    for caracter in pwd:
        if caracter.isupper():
            mayuscula = True
        if caracter.isdigit():
            digito = True
        if not (especiales.search(caracter) == None): 
            especial = True
        
    if(mayuscula and digito and especial and caracter):
        return True
    
    return False


class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')
        model = Usuario

    def create(self, validated_data):
        validar = validar_pwd(validated_data['password'])
        if validar:
            validated_data['password'] = make_password(
                validated_data.get('password'))
            validated_data['username'] = validated_data["email"]
            return super(UsuarioSerializer, self).create(validated_data)
        raise serializers.ValidationError({'password': 
            'The password must include at least one: upper case letter, upper case letter, digit, special character'})