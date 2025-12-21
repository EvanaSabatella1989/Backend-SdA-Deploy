from rest_framework import serializers
from django.conf import settings
from .models import Producto
from venta_detalle.models import VentaDetalle

class VentaDetalleSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = VentaDetalle
        fields = [
            'producto_nombre',
            'cantidad',
            'precio',
            'descuento'
        ]
