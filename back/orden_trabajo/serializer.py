from rest_framework import serializers
from orden_trabajo.models import OrdenTrabajo
from reserva.serializer import ReservaSerializer




class OrdenTrabajoSerializer(serializers.ModelSerializer):
    reserva_id = serializers.IntegerField(write_only=True, required=False)
    vehiculo_id = serializers.IntegerField(write_only=True)
    empleado_id = serializers.IntegerField(write_only=True, required=False)

    #  los originales
    # reserva = serializers.StringRelatedField(read_only=True)
    reserva = ReservaSerializer(read_only=True)
    vehiculo = serializers.StringRelatedField(read_only=True)
    empleado = serializers.StringRelatedField(read_only=True)

    # info extra SIN romper nada
    empleado_nombre = serializers.SerializerMethodField()
    vehiculo_info = serializers.SerializerMethodField()
    cliente_info = serializers.SerializerMethodField()

    class Meta:
        model = OrdenTrabajo
        fields = [
            'id',

            # originales
            'reserva',
            'vehiculo',
            'empleado',

            # extras
            'empleado_nombre',
            'vehiculo_info',
            'cliente_info',

            # write only
            'reserva_id',
            'vehiculo_id',
            'empleado_id',

            # propios
            'fecha_ingreso',
            'fecha_egreso',
            'diagnostico',
            'observaciones',
            'estado',
        ]

    def get_empleado_nombre(self, obj):
        if obj.empleado and obj.empleado.user:
            return obj.empleado.user.get_full_name()
        return None

    def get_vehiculo_info(self, obj):
        if obj.vehiculo:
            return {
                "marca": obj.vehiculo.marca,
                "modelo": obj.vehiculo.modelo,

            }
        return None

    def get_cliente_info(self, obj):
        if obj.reserva and obj.reserva.cliente and obj.reserva.cliente.user:
            return {
                "nombre": obj.reserva.cliente.user.first_name,
                "apellido": obj.reserva.cliente.user.last_name,
            }
        return None

    def create(self, validated_data):
        reserva_id = validated_data.pop('reserva_id', None)
        vehiculo_id = validated_data.pop('vehiculo_id')
        empleado_id = validated_data.pop('empleado_id', None)

        from reserva.models import Reserva
        from vehiculo.models import Vehiculo
        from user.models import Empleado

        if reserva_id:
            validated_data['reserva'] = Reserva.objects.get(id=reserva_id)

        validated_data['vehiculo'] = Vehiculo.objects.get(id=vehiculo_id)

        if empleado_id:
            validated_data['empleado'] = Empleado.objects.get(id=empleado_id)

        return OrdenTrabajo.objects.create(**validated_data)

# para llamar en perfil para ver los servicios
class OrdenTrabajoSerializerDos(serializers.ModelSerializer):
    servicio_nombre = serializers.CharField(
        source='reserva.servicio.nombre', read_only=True
    )
    turno_fecha = serializers.DateField(
        source='reserva.turno.fecha', read_only=True
    )
    turno_hora = serializers.TimeField(
        source='reserva.turno.hora', read_only=True
    )

    class Meta:
        model = OrdenTrabajo
        fields = [
            'id',
            'estado',
            'fecha_ingreso',
            'fecha_egreso',
            'diagnostico',
            'observaciones',
            'servicio_nombre',
            'turno_fecha',
            'turno_hora',
        ]