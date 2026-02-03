from django.db import models
from user.models import Cliente
from sucursal.models import Sucursal
from servicio.models import Servicio
from turno.models import Turno
from vehiculo.models import Vehiculo

class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE,null=True, blank=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE, null=True, blank=True)  
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, null=True, blank=True)  
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE,null=True, blank=True)
    estado = models.CharField(max_length=20, choices=[
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('reprogramada', 'Reprogramada'),
        ('cancelada', 'Cancelada')
    ], default='pendiente')

    def __str__(self):
        return f"Reserva de {self.cliente} para {self.servicio} en {self.turno}"





# from sucursal.models import Sucursal
# from servicio.models import Servicio
# from sucursal.models import HorarioSucursal

# class Reserva(models.Model):
#     # usuario = models.ForeignKey(User, on_delete=models.CASCADE)
#     sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
#     servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
#     hora_sucursal = models.ForeignKey(HorarioSucursal, on_delete=models.CASCADE,related_name='reservas_fecha',default=1 )
#     fecha_sucursal=models.ForeignKey(HorarioSucursal,on_delete=models.CASCADE,related_name='reservas_hora',default=1 )
#     nombre_cliente = models.CharField(max_length=100)
#     correo_cliente = models.EmailField(default='default@example.com')


# class Meta:
#     db_table = "reserva"
#     verbose_name_plural = "reservas"
#     verbose_name = "reserva"


#     def __str__(self):
#         return f"Reserva de {self.nombre_cliente} en {self.sucursal.nombre} el {self.hora_sucursal.hora} a las {self.fecha_sucursal.fecha} para el servicio de {self.servicio.nombre}"

