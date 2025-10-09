from rest_framework import serializers
from .models import Sucursal
from servicio.models import Servicio

# from sucursal.models import HorarioSucursal


# para realizar post put con id
class SucursalWriteSerializer(serializers.ModelSerializer):
    servicios = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Servicio.objects.all(),
        required=False
    )
    
    class Meta:
        model = Sucursal
        fields = ['id', 'nombre', 'direccion', 'telefono', 'servicios']

# solo get trae todos los datos del servicio
class ServicioMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'precio']
        
        

class SucursalReadSerializer(serializers.ModelSerializer):
    servicios = ServicioMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Sucursal
        fields = ['id', 'nombre', 'direccion', 'telefono', 'servicios']