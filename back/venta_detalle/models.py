from django.db import models
from venta.models import Venta
from producto.models import Producto
from datetime import datetime

# Create your models here.


class VentaDetalle(models.Model):
    precio = models.DecimalField(max_digits=15, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    descuento = models.DecimalField(max_digits=10, decimal_places=2)
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    class Meta:
        db_table = "ventadetalle"
        verbose_name_plural = "ventadetalles"
        verbose_name = "ventadetalle"

    def __str__(self):
        return self.venta
