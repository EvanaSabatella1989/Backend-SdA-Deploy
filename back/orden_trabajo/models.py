from django.db import models
from reserva.models import Reserva
from vehiculo.models import Vehiculo
from user.models import Empleado


class OrdenTrabajo(models.Model):
    reserva = models.OneToOneField(Reserva,on_delete=models.SET_NULL,null=True,blank=True,related_name='orden_trabajo')
    vehiculo = models.ForeignKey(Vehiculo,on_delete=models.CASCADE,related_name='ordenes_trabajo')
    empleado = models.ForeignKey(Empleado,on_delete=models.SET_NULL,null=True,blank=True,related_name='ordenes_asignadas')
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_egreso = models.DateTimeField(null=True, blank=True)
    diagnostico = models.TextField(blank=True)
    observaciones = models.TextField(blank=True)

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('finalizado', 'Finalizado'),
        ('entregado', 'Entregado'),
    ]

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente'
    )

    def __str__(self):
        reserva_id = self.reserva.id if self.reserva else "Sin reserva"
        return f"OrdenTrabajo #{self.id} - Reserva: {reserva_id}"
