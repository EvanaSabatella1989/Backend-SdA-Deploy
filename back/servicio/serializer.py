from rest_framework import serializers
from .models import Servicio
from categoria.models import Categoria
from sucursal.serializers import SucursalReadSerializer


# trae solo los id de los atributos
class ServicioSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(required=False)  #  que la imagen no sea obligatoria
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())
    class Meta:
        model=Servicio
        fields='__all__'
        depth = 1
        


#para que traiga el nombre de los atributos del servicio    
class ServicioNombreSerializer(serializers.ModelSerializer):
    categoriaNombre = serializers.CharField(source='categoria.nombre', read_only=True)

    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'descripcion', 'precio', 'imagen', 'categoria', 'categoriaNombre']


# para que me traiga la sucursal relacionada
class ServicioConSucursalesSerializer(serializers.ModelSerializer):
    sucursales = SucursalReadSerializer(many=True, read_only=True)  # trae id, nombre, direccion, etc.
    categoriaNombre = serializers.CharField(source='categoria.nombre', read_only=True)

    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'descripcion', 'precio', 'imagen', 'categoria', 'categoriaNombre', 'sucursales']