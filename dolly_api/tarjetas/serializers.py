from rest_framework import serializers
from tarjetas.models import Tarjeta

class TarjetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarjeta
        fields = '__all__'