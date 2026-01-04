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
    cliente_id = serializers.IntegerField(source='cliente.id', read_only=True)

    cliente_nombre = serializers.CharField(
        source='cliente.user.first_name',
        read_only=True
    )
    cliente_apellido = serializers.CharField(
        source='cliente.user.last_name',
        read_only=True
    )
    detalles = VentaDetalleSerializer(
        source='ventadetalle_set',
        many=True,
        read_only=True
    )

    class Meta:
        model = Venta
        fields = '__all__'
