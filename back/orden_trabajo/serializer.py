from rest_framework import serializers
from orden_trabajo.models import OrdenTrabajo





class OrdenTrabajoSerializer(serializers.ModelSerializer):

    reserva_id = serializers.IntegerField(write_only=True, required=False)
    vehiculo_id = serializers.IntegerField(write_only=True)
    empleado_id = serializers.IntegerField(write_only=True, required=False)

    reserva = serializers.StringRelatedField(read_only=True)
    vehiculo = serializers.StringRelatedField(read_only=True)
    empleado = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = OrdenTrabajo
        fields = [
            'id',
            'reserva',
            'vehiculo',
            'empleado',
            'reserva_id',
            'vehiculo_id',
            'empleado_id',
            'fecha_ingreso',
            'fecha_egreso',
            'diagnostico',
            'observaciones',
            'estado',
        ]

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