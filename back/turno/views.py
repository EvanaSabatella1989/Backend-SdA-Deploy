from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Turno
from .serializers import TurnoSerializer
from django.http import JsonResponse


class TurnoViewSet(viewsets.ModelViewSet):
    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer

# 
    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        sucursal_id = request.query_params.get('sucursal')
        fecha = request.query_params.get('fecha')
        turnos = Turno.objects.filter(disponible=True)

        if sucursal_id:
            turnos = turnos.filter(sucursal_id=sucursal_id)
        if fecha:
            turnos = turnos.filter(fecha=fecha)

        serializer = TurnoSerializer(turnos, many=True)
        return Response(serializer.data)


    # endpoint para turnos disponibles por sucursal
    @action(detail=False, methods=['get'], url_path='disponibles-por-sucursal')
    def disponibles_por_sucursal(self, request):
        sucursal_id = request.query_params.get('sucursal')
        if not sucursal_id:
            return Response([])

        # solo turnos libres
        turnos = Turno.objects.filter(
            sucursal_id=sucursal_id,
            disponible=True
        ).order_by('fecha', 'hora')

        serializer = TurnoSerializer(turnos, many=True)
        return Response(serializer.data)