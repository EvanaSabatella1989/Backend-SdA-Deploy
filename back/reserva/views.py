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

    
# SE ENVIA LA RESERVA AL CORREO DEL ADMIN Y CLIENTE
# TAMBIEN SE CONFIRMA LA RESERVA Y SE ENVIA LOS DATOS A LA DB Y EL TURNO DISPONIBLE PASA A FALSE
    def perform_create(self, serializer):
        logger.debug(f"📥 Datos validados recibidos: {serializer.validated_data}")
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
            correo_cliente = cliente.user.email

            # MAIL ADMIN
            mensaje_admin = f"""
    Nueva reserva registrada.

    Cliente: {nombre_cliente}
    Correo: {correo_cliente}

    Servicio: {reserva.servicio.nombre}
    Fecha: {turno.fecha}
    Hora: {turno.hora}
    Sucursal: {turno.sucursal.nombre}
    """

            send_mail(
                'Nueva Reserva de Turno',
                mensaje_admin,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            # MAIL CLIENTE
            mensaje_cliente = f"""
    Hola {nombre_cliente},

    ¡Gracias por reservar en Service del Automotor! 🚗🔧

    📌 Servicio: {reserva.servicio.nombre}
    📅 Fecha: {turno.fecha}
    ⏰ Hora: {turno.hora}
    🏢 Sucursal: {turno.sucursal.nombre}

    ¡Te esperamos!
    """

            send_mail(
                'Confirmación de tu reserva',
                mensaje_cliente,
                settings.DEFAULT_FROM_EMAIL,
                [correo_cliente],
                fail_silently=False,
            )

            logger.info(f"📧 Correos enviados para reserva ID={reserva.id}")

        except Exception as e:
            logger.exception(f"Error creando reserva: {str(e)}")
            raise


def enviar_mail_reserva(subject, message, recipient_list):
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"❌ Error enviando correo async: {str(e)}")

