from rest_framework import serializers, validators
from django.contrib.auth import get_user_model
User = get_user_model()
from vehiculo.serializers import VehiculoSerializer
from carrito.serializers import CarritoSerializer
from user.models import Cliente
from reserva.serializer import ReservaSerializer
from vehiculo.serializers import VehiculoReservaSerializer

class UserSerializer(serializers.ModelSerializer):
    vehiculos = VehiculoSerializer(many=True, read_only=True, source="cliente.vehiculo_set")
    carrito = CarritoSerializer(read_only=True, source="cliente.carrito")
    reservas = ReservaSerializer(many=True, read_only=True, source="cliente.reserva_set")
    class Meta():
        model = User
        fields = ("id", "email", "first_name", "last_name", "password", 'vehiculos', 'carrito', 'reservas')
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), f"Ya existe un usuario con este correo electrónico."
                    )
                ],
            },
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"]
        )
        
        #para poder crear usuario en angular
        Cliente.objects.get_or_create(user=user, defaults={'direccion': '', 'num_telefono': ''})
        
        return user
    

class ClienteSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name',  required=False)
    last_name = serializers.CharField(source='user.last_name',  required=False)
    direccion = serializers.CharField(required=False, allow_blank=True)
    num_telefono = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Cliente
        fields = ['id', 'email', 'first_name', 'last_name', 'direccion', 'num_telefono']

    def update(self, instance, validated_data):
        # aca agregamos los datos del cliente que se quiera editar
        instance.direccion = validated_data.get('direccion', instance.direccion)
        instance.num_telefono = validated_data.get('num_telefono', instance.num_telefono)
        instance.save()
        
        # aca agregamos los datos del usuario relacionado al cliente para editar
        user_data = validated_data.get('user', {})
        if user_data:
            user = instance.user
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.save()
            
        return instance
    

# para usar en reserva
class UserReservaSerializer(serializers.ModelSerializer):
    vehiculos = VehiculoReservaSerializer(many=True, read_only=True, source="cliente.vehiculo_set")

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "vehiculos"]