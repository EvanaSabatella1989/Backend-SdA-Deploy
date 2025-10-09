from django.db import models
from sucursal.models import Sucursal
from servicio.models import Servicio

class Turno(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    # servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name="turnos",null=True, blank=True)
    fecha = models.DateField()
    hora = models.TimeField()
    disponible = models.BooleanField(default=True)  

    class Meta:
        unique_together = ('sucursal', 'fecha', 'hora')  

    def __str__(self):
        return f"{self.sucursal} - {self.fecha} {self.hora}"
