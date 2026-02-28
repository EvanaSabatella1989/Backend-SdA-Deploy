from rest_framework import viewsets
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from orden_trabajo.models import OrdenTrabajo
from orden_trabajo.serializer import OrdenTrabajoSerializer


class OrdenTrabajoViewSet(viewsets.ModelViewSet):
    queryset = OrdenTrabajo.objects.all()
    serializer_class = OrdenTrabajoSerializer


#vista para el empleado
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def mis_trabajos(request):
        empleado = request.user.empleado
        ordenes = OrdenTrabajo.objects.filter(empleado=empleado)
        serializer = OrdenTrabajoSerializer(ordenes, many=True)
        return Response(serializer.data)