from django.db import models
from usuarios.models import Usuario
import uuid

# Create your models here.
class Tablero(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    dueño = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    favorito = models.BooleanField(default=False)
    visibilidad = models.BooleanField(default=False)
    miembros = models.ManyToManyField(Usuario, related_name='miembros')

    def __str__(self):
        return self.nombre
