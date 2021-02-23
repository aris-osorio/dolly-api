from django.db import models
from tarjetas.models import Tarjeta
from usuarios.models import Usuario
import uuid


# Create your models here.
class Comentario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tarjeta = models.ForeignKey(Tarjeta, on_delete = models.CASCADE)
    mensaje = models.CharField(max_length = 200)
    dueño = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.mensaje
