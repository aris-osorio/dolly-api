from django.db import models
from tableros.models import Tablero
import uuid

# Create your models here.
class Lista(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=200)
    tablero = models.ForeignKey(Tablero, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    posicion = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.nombre