from rest_framework import viewsets
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from orden_trabajo.models import OrdenTrabajo
from orden_trabajo.serializer import OrdenTrabajoSerializer
from rest_framework.decorators import action

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
    @action(detail=True, methods=['post'], url_path='cambiar-estado')
    def cambiar_estado(self, request, pk=None):
        orden = self.get_object()
        user = request.user

        # Si no es admin, validamos que sea su orden
        if not user.is_staff:
            try:
                empleado = user.empleado
            except:
                return Response({"detail": "No autorizado"}, status=403)

            if orden.empleado != empleado:
                return Response({"detail": "No es tu orden"}, status=403)

        nuevo_estado = request.data.get("estado")

        if nuevo_estado not in dict(OrdenTrabajo.ESTADOS):
            return Response({"detail": "Estado inválido"}, status=400)

        orden.estado = nuevo_estado
        orden.save()

        return Response({"detail": "Estado actualizado"})