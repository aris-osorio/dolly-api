from comentarios.models import Comentario
from rest_framework import serializers

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'