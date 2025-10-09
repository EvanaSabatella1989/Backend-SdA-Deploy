from django.db import models
from user.models import Cliente
# from user.models import UserAccount
from datetime import datetime
from categoria.models import Categoria

# Create your models here.


class Vehiculo(models.Model):
    marca = models.CharField(max_length=100, default="Desconocido")  # Nueva columna ejemplo Honda, Yamaha
    modelo = models.CharField(max_length=100)  #ejemplo Civic, YZF-R3
    # categoria = models.CharField(max_length=100, default="Desconocido")  # Nueva columna (Ej: Moto, Auto, Camión)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vehiculos"
    )
    tipo = models.CharField(max_length=100, default="Otro") # ejemplo autos(sedán, pickup) ejemplo moto (deportiva, scooter, enduro)
    anio_fabricacion = models.PositiveIntegerField(default=2000)  # Nueva columna
    # imagen = models.ImageField(upload_to='photos/%Y/%m/')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = "vehiculo"
        verbose_name_plural = "vehiculos"
        verbose_name = "vehiculo"

    def get_thumbnail(self):
        if self.imagen:
            return self.imagen.url
        return ''

    def __str__(self):
        # return self.modelo
        return f"{self.marca} {self.modelo} ({self.anio_fabricacion})"