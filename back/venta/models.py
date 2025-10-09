from django.db import models
from datetime import datetime
from user.models import Cliente

# Create your models here.


class Venta(models.Model):

    numero_factura = models.BigIntegerField()
    total = models.DecimalField(max_digits=15, decimal_places=2) 
    TIPOS_PAGO = (
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta de crédito'),
        ('transferencia', 'Transferencia bancaria'),
    )

    ESTADOS_VENTA = (
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    )
    tipo_pago = models.CharField(max_length=20, choices=TIPOS_PAGO)
    estado = models.CharField(max_length=20, choices=ESTADOS_VENTA)
    fecha_pago = models.DateTimeField(default=datetime.now)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    class Meta:
        db_table = "venta"
        verbose_name_plural = "ventas"
        verbose_name = "venta"

    def __str__(self):
        return self.numero_factura
