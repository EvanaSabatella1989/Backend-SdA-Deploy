from rest_framework import serializers
from rest_framework import serializers
from .models import Reserva,Turno,Servicio,Vehiculo
from user.models import Cliente
# from user.serializers import ClienteSerializer
from servicio.serializer import ServicioSerializer
from turno.serializers import TurnoSerializer

# class ReservaSerializer(serializers.ModelSerializer):
#     cliente = ClienteSerializer(read_only=True)
#     # servicio = ServicioSerializer(read_only=True)
#     servicio=serializers.PrimaryKeyRelatedField(queryset=Servicio.objects.all())
#     turno = serializers.PrimaryKeyRelatedField(queryset=Turno.objects.all())
    
#     # Campos calculados para la lista
#     # servicio_info = serializers.SerializerMethodField()
#     # turno_info = serializers.SerializerMethodField()
#     # sucursal_info = serializers.SerializerMethodField()

#     class Meta:
#         model = Reserva
#         fields = '__all__'
#         # fields = ['id', 'cliente', 'servicio', 'servicio_info', 'turno', 'turno_info', 'sucursal_info', 'estado']
        
#     def get_turno(self, obj):
#         if obj.turno:
#             return {
#                 "id": obj.turno.id,
#                 "fecha": obj.turno.fecha,
#                 "hora": obj.turno.hora
#             }
#         return None

#     def get_sucursal(self, obj):
#         if obj.servicio and obj.servicio.sucursal:
#             return {
#                 "id": obj.servicio.sucursal.id,
#                 "nombre": obj.servicio.sucursal.nombre
#             }
#         return None
    
#     def get_servicio_info(self, obj):
#         if obj.servicio:
#             return {
#                 "id": obj.servicio.id,
#                 "nombre": obj.servicio.nombre
#             }
#         return None

class ReservaSerializer(serializers.ModelSerializer):
    cliente = serializers.SerializerMethodField()
    servicio = serializers.PrimaryKeyRelatedField(queryset=Servicio.objects.all())
    turno = serializers.PrimaryKeyRelatedField(queryset=Turno.objects.all())
    vehiculo = serializers.PrimaryKeyRelatedField(queryset=Vehiculo.objects.all(), required=False)
    
    # Campos calculados para la lista
    servicio_info = serializers.SerializerMethodField()
    turno_info = serializers.SerializerMethodField()
    sucursal_info = serializers.SerializerMethodField()
    vehiculo_info = serializers.SerializerMethodField()

    class Meta:
        model = Reserva
        fields = [
            'id',
            'cliente',
            'servicio',
            'servicio_info',
            'turno',
            'turno_info',
            'sucursal_info',
            'vehiculo',        
            'vehiculo_info',
            'estado'
        ]
        depth = 2  # para expandir turno y sucursal

    def get_cliente(self, obj):
        from user.serializers import ClienteSerializer  # 👈 import local para evitar circular import
        return ClienteSerializer(obj.cliente).data if obj.cliente else None

    def get_servicio_info(self, obj):
        if obj.servicio:
            return {
                "id": obj.servicio.id,
                "nombre": obj.servicio.nombre
            }
        return None

    def get_turno_info(self, obj):
        if obj.turno:
            return {
                "id": obj.turno.id,
                "fecha": obj.turno.fecha,
                "hora": obj.turno.hora
            }
        return None

    def get_sucursal_info(self, obj):
        if obj.turno and obj.turno.sucursal:
            return {
                "id": obj.turno.sucursal.id,
                "nombre": obj.turno.sucursal.nombre
            }
        return None
    
    def get_vehiculo_info(self, obj):
        if obj.vehiculo:
            return {
                "id": obj.vehiculo.id,
                "marca": obj.vehiculo.marca,
                "modelo": obj.vehiculo.modelo,
                "anio": obj.vehiculo.anio_fabricacion,
                "categoria": {
                    "id": obj.vehiculo.categoria.id,
                    "nombre": obj.vehiculo.categoria.nombre,
                    "tipo": obj.vehiculo.categoria.tipo
                } if obj.vehiculo.categoria else None
            }