from rest_framework import serializers
from .models import Venta

class VentaSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Venta
        fields = '__all__'
