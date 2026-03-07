from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Turno
from .serializers import TurnoSerializer
from django.http import JsonResponse
from datetime import time
from django.utils import timezone
from datetime import date, datetime

class TurnoViewSet(viewsets.ModelViewSet):
    # queryset = Turno.objects.all()
    # serializer_class = TurnoSerializer
    serializer_class = TurnoSerializer
    # mostrar solo turnos del dia o futuros, no vencidos
    def get_queryset(self):
        from django.utils import timezone
        ver_todos = self.request.query_params.get('ver_todos', 'false')

        if ver_todos == 'true':
            return Turno.objects.all().order_by('fecha', 'hora')

        ahora = timezone.localtime(timezone.now())
        return Turno.objects.filter(
            fecha__gte=ahora.date()
        ).exclude(
            fecha=ahora.date(), hora__lt=ahora.time()
        ).order_by('fecha', 'hora')

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

        ahora = timezone.localtime(timezone.now())
        hoy = ahora.date()
        hora_actual = ahora.time()


        # solo turnos libres
        turnos = Turno.objects.filter(
            sucursal_id=sucursal_id,
            disponible=True,
        fecha__gte = hoy
        ).exclude(
            fecha=hoy, hora__lt=hora_actual
        ).order_by('fecha', 'hora')

        serializer = TurnoSerializer(turnos, many=True)
        return Response(serializer.data)

    # que sean turnos con horarios restringidos 9 a 18
    @action(detail=False, methods=['post'], url_path='generar-turnos')
    def generar_turnos(self, request):
        sucursal_id = request.data.get('sucursal_id')
        fecha = request.data.get('fecha')  # formato: "2025-01-15"

        if not sucursal_id or not fecha:
            return Response({"detail": "Faltan datos"}, status=400)

        horarios = [time(hora, 0) for hora in range(9, 18)]  # 9:00 a 17:00
        creados = 0

        for hora in horarios:
            _, creado = Turno.objects.get_or_create(
                sucursal_id=sucursal_id,
                fecha=fecha,
                hora=hora,
                defaults={'disponible': True}
            )
            if creado:
                creados += 1

        return Response({"detail": f"{creados} turnos creados"})