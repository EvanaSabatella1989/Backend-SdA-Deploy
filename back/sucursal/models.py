from django.db import models
from django.core.validators import RegexValidator
from datetime import time
from datetime import date
from servicio.models import Servicio

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, default='')
    ciudad = models.CharField(max_length=100, default='', blank=True)
    provincia = models.CharField(max_length=100, default='', blank=True)
    servicios = models.ManyToManyField(Servicio, related_name="sucursales", blank=True)

    class Meta:
        db_table = "sucursal"
        verbose_name_plural = "sucursales"
        verbose_name = "sucursal"

    def __str__(self):
        return self.nombre

