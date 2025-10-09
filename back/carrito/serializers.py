# from rest_framework import serializers
# from .models import Carrito, CarritoItem

# class CarritoItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CarritoItem
#         fields = '__all__'

# class CarritoSerializer(serializers.ModelSerializer):
#     items = CarritoItemSerializer(many=True)

#     class Meta:
#         model = Carrito
#         fields = '__all__'

from rest_framework import serializers
from .models import Carrito, CarritoItem
from producto.models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'imagen', 'descripcion', 'precio', 'categoria', 'cantidad']

class CarritoItemSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()  # Incluye todos los detalles del producto

    class Meta:
        model = CarritoItem
        fields = ['id', 'producto', 'cantidad']

class CarritoSerializer(serializers.ModelSerializer):
    items = CarritoItemSerializer(many=True)

    class Meta:
        model = Carrito
        fields = ['id', 'user', 'items']