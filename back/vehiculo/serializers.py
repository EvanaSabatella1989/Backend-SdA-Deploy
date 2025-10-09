from rest_framework import serializers
from .models import Vehiculo
from categoria.models import Categoria

class VehiculoSerializer(serializers.ModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())
    class Meta:
        model = Vehiculo
        fields = '__all__'
        # fields = ['id', 'marca', 'modelo', 'categoria', 'tipo', 'anio_fabricacion', 'cliente']
        

# para la reserva
class VehiculoReservaSerializer(serializers.ModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(read_only=True)  
    class Meta:
        model = Vehiculo
        fields = ['id', 'marca', 'modelo', 'tipo', 'anio_fabricacion', 'categoria']