from rest_framework import serializers
from django.conf import settings
from .models import Producto
from categoria.models import Categoria

class ProductoSerializer(serializers.ModelSerializer):
    # 🔹 Forzamos a que interprete 'categoria' como un ID válido de Categoria
    categoria = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all()
    )

    class Meta:
        model=Producto
        fields='__all__' #,['nombre','imagen','descripcion','precio','categoria','cantidad','date_created']
        extra_kwargs = {
            'imagen': {'required': False, 'allow_null': True}
        }
        depth = 1

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "El precio debe ser mayor a 0"
            )
        return value
    
    def validate_cantidad(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "La cantidad debe ser un número entero mayor a 0"
            )
        return value
        
    def create(self, validated_data):
        print("validated_data:", validated_data)
        return super().create(validated_data)