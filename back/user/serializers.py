from rest_framework import serializers, validators
from django.contrib.auth import get_user_model
User = get_user_model()
from vehiculo.serializers import VehiculoSerializer
from carrito.serializers import CarritoSerializer
from user.models import Cliente,Empleado, UserAccount
from reserva.serializer import ReservaSerializer
from vehiculo.serializers import VehiculoReservaSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
import re


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

        # para poder crear usuario en angular
        Cliente.objects.get_or_create(user=user, defaults={'direccion': '', 'num_telefono': ''})

        return user


class ClienteSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
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
        
    
#  para doble paassword obligatorio
class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def validate(self, data):
        password = data['password1']

        # bloquear solo letras
        if re.fullmatch(r'[a-zA-Z]+', password):
            raise serializers.ValidationError({
                "password1": "La contraseña no puede contener solo letras."
            })

        # contraseñas distintas
        if password != data['password2']:
            raise serializers.ValidationError({
                "password2": "Las contraseñas no coinciden"
            })

        # validadores Django común,similar,numérica
        try:
            validate_password(password)
        except DjangoValidationError as e:
            raise serializers.ValidationError({
                "password1": e.messages
            })

        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')

        user = User.objects.create_user(
            email=validated_data['email'],
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        Cliente.objects.get_or_create(
            user=user,
            defaults={'direccion': '', 'num_telefono': ''}
        )

        return user



#Crear serializer JWT custom
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 👇 AGREGAMOS INFO DE ROL
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        token['email'] = user.email

        return token

#para crear al empleado
class EmpleadoCreateSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    class Meta:
        model = Empleado
        fields = [
            'id',
            'cargo',
            'email',
            'password',
            'first_name',
            'last_name'
        ]

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')

        user = UserAccount.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_client=False,
            is_staff=True  # si querés que pueda entrar al admin
        )

        empleado = Empleado.objects.create(
            user=user,
            **validated_data
        )

        return empleado

    #para leer empleado
class EmpleadoSerializer(serializers.ModelSerializer):
        first_name = serializers.CharField(source='user.first_name', read_only=True)
        last_name = serializers.CharField(source='user.last_name', read_only=True)
        email = serializers.CharField(source='user.email', read_only=True)

        class Meta:
            model = Empleado
            fields = [
                'id',
                'cargo',
                'first_name',
                'last_name',
                'email'
            ]
#para editar
class EmpleadoUpdateSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Empleado
        fields = [
            'cargo',
            'first_name',
            'last_name',
            'email'
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')

        # actualizar empleado
        instance.cargo = validated_data.get('cargo', instance.cargo)
        instance.save()

        # actualizar usuario
        user = instance.user
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.save()

        return instance