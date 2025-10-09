from django.shortcuts import render
from rest_framework import viewsets, status
from reserva.models import Reserva
from .models import Sucursal
# from .serializers import SucursalSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import logging
from django.shortcuts import render,get_object_or_404
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from django.db.models import Prefetch
from sucursal.serializers import SucursalReadSerializer,SucursalWriteSerializer,ServicioMiniSerializer
# from sucursal.models import HorarioSucursal
from rest_framework.decorators import action
from servicio.serializer import ServicioNombreSerializer

logger = logging.getLogger(__name__)

class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return SucursalReadSerializer   # devuelve nombres de servicios
        return SucursalWriteSerializer      # recibe IDs de servicios


 # endpoint para sucursales por servicio
    # @action(detail=False, methods=['get'], url_path='por-servicio')
    # def por_servicio(self, request):
    #     servicio_id = request.query_params.get('servicio_id')
    #     sucursales = Sucursal.objects.filter(servicios__id=servicio_id)
    #     serializer = SucursalReadSerializer(sucursales, many=True)
    #     return Response(serializer.data)
    @action(detail=False, methods=['get'], url_path='por-servicio')
    def por_servicio(self, request):
        servicio_id = request.query_params.get('servicio_id')

        if not servicio_id:
            return Response({"error": "Falta servicio_id"}, status=400)

        try:
            servicio_id = int(servicio_id)
        except ValueError:
            return Response({"error": "servicio_id debe ser un número"}, status=400)

        sucursales = Sucursal.objects.filter(servicios__id=servicio_id).distinct()  # distinct por si hay duplicados
        serializer = SucursalReadSerializer(sucursales, many=True)
        return Response(serializer.data)



    # para ver los servicios que tiene cada sucursal
    @action(detail=True, methods=['get'])
    def servicios(self, request, pk=None):
        sucursal = self.get_object()
        servicios = sucursal.servicios.all()
        serializer = ServicioNombreSerializer(servicios, many=True)
        return Response(serializer.data)