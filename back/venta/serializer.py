from rest_framework import serializers
from .models import Venta
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


class VentaSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(read_only=True)
    detalles = VentaDetalleSerializer(
        source='ventadetalle_set',
        many=True,
        read_only=True
    )

    class Meta:
        model = Venta
        fields = '__all__'
