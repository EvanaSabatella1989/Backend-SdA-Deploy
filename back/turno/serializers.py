from rest_framework import serializers
from .models import Turno, Sucursal
from sucursal.serializers import SucursalWriteSerializer

class TurnoSerializer(serializers.ModelSerializer):
    sucursal = SucursalWriteSerializer(read_only=True)
    sucursal_id = serializers.PrimaryKeyRelatedField(queryset=Sucursal.objects.all(), source='sucursal', write_only=True)

    class Meta:
        model = Turno
        fields = '__all__'




      