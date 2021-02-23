from listas.models import Lista
from rest_framework import serializers

class ListaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lista
        fields = '__all__'