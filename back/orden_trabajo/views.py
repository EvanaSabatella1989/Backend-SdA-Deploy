from rest_framework import viewsets
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from orden_trabajo.models import OrdenTrabajo
from orden_trabajo.serializer import OrdenTrabajoSerializer,OrdenTrabajoSerializerDos
from rest_framework.decorators import action
from django.utils import timezone

class OrdenTrabajoViewSet(viewsets.ModelViewSet):
    #queryset = OrdenTrabajo.objects.all()
    serializer_class = OrdenTrabajoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Si es admin
        if user.is_staff:
            return OrdenTrabajo.objects.all()

        # Si es empleado
        try:
            empleado = user.empleado
            return OrdenTrabajo.objects.filter(empleado=empleado)
        except:
            return OrdenTrabajo.objects.none()

    #ve las ordenes
    @action(detail=False, methods=['get'], url_path='mis-trabajos')
    def mis_trabajos(self, request):
        try:
            empleado = request.user.empleado
        except:
            return Response({"detail": "No autorizado"}, status=403)

        ordenes = OrdenTrabajo.objects.filter(empleado=empleado)
        serializer = self.get_serializer(ordenes, many=True)
        return Response(serializer.data)

    #cambia el estado
    @action(detail=True, methods=['patch'], url_path='cambiar-estado')
    def cambiar_estado(self, request, pk=None):
        orden = self.get_object()
        user = request.user

        if not user.is_staff:
            try:
                empleado = user.empleado
            except AttributeError:
                return Response({"detail": "No autorizado"}, status=403)

            if orden.empleado != empleado:
                return Response({"detail": "No es tu orden"}, status=403)

        nuevo_estado = request.data.get("estado")

        if nuevo_estado not in dict(OrdenTrabajo.ESTADOS):
            return Response({"detail": "Estado inválido"}, status=400)

        orden.estado = nuevo_estado

        # Auto fecha_egreso al finalizar o entregar
        if nuevo_estado in ('finalizado', 'entregado') and not orden.fecha_egreso:
            orden.fecha_egreso = timezone.now()

        orden.save()

        return Response({"detail": "Estado actualizado"})

    # editar el contenido de la orden
    @action(detail=True, methods=['patch'], url_path='actualizar-orden')
    def actualizar_orden(self, request, pk=None):
        orden = self.get_object()
        user = request.user

        if not user.is_staff:
            try:
                empleado = user.empleado
            except AttributeError:
                return Response({"detail": "No autorizado"}, status=403)

            if orden.empleado != empleado:
                return Response({"detail": "No es tu orden"}, status=403)

        # Solo permitimos editar estos campos
        campos_permitidos = ['diagnostico', 'observaciones', 'estado']
        data = {k: v for k, v in request.data.items() if k in campos_permitidos}

        serializer = self.get_serializer(orden, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


    # para que el usuario vea el estado del servicio realizado
    @action(detail=False, methods=['get'], url_path='por-vehiculo')
    def por_vehiculo(self, request):
        vehiculo_id = request.query_params.get('vehiculo')
        if not vehiculo_id:
            return Response({"detail": "Falta el parámetro vehiculo"}, status=400)

        ordenes = OrdenTrabajo.objects.filter(
            vehiculo_id=vehiculo_id,
            vehiculo__cliente__user=request.user
        ).select_related('reserva__servicio', 'reserva__turno', 'empleado__user')

        print("ordenes encontradas:", ordenes.count())
        for o in ordenes:
            print("orden:", o.id, "vehiculo:", o.vehiculo_id, "cliente user:", o.vehiculo.cliente.user)

        serializer = OrdenTrabajoSerializerDos(ordenes, many=True)
        return Response(serializer.data)