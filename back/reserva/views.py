from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from django.core.mail import send_mail
from .serializer import ReservaSerializer
from .models import Reserva,Turno
import logging
from django.conf import settings
from datetime import datetime, timedelta
# from sucursal.models import HorarioSucursal
from rest_framework import status
from django.conf import settings
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from user.models import Cliente
import threading
from django.core.mail import send_mail
from django.conf import settings



logger = logging.getLogger(__name__)

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated] 

    

# TAMBIEN SE CONFIRMA LA RESERVA Y SE ENVIA LOS DATOS A LA DB Y EL TURNO DISPONIBLE PASA A FALSE
    def perform_create(self, serializer):
        logger.debug(f" Datos validados recibidos: {serializer.validated_data}")
        self.reservar_turno(serializer)

    def reservar_turno(self, serializer):
        try:
            user = self.request.user
            cliente = Cliente.objects.get(user=user)
            turno = serializer.validated_data['turno']

            if not turno.disponible:
                raise serializers.ValidationError("Este horario ya está reservado")

            turno.disponible = False
            turno.save()

            reserva = serializer.save(
                cliente=cliente,
                sucursal=turno.sucursal
            )

            nombre_cliente = cliente.user.get_full_name()

            logger.info(f"Reserva creada con éxito ID={reserva.id}")

            # MENSAJE WHATSAPP
            mensaje_whatsapp = (
                f"Hola, soy {nombre_cliente}.\n\n"
                f"Reservé un turno:\n"
                f"🛠 Servicio: {reserva.servicio.nombre}\n"
                f"📅 Fecha: {turno.fecha}\n"
                f"⏰ Hora: {turno.hora}\n"
                f"📍 Sucursal: {turno.sucursal.nombre}\n\n"
                f"Gracias."
            )

            return Response(
                {
                    "reserva_id": reserva.id,
                    "mensaje_whatsapp": mensaje_whatsapp
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            logger.exception(f"Error creando reserva: {str(e)}")
            raise


