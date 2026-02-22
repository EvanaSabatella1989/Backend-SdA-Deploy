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
from rest_framework.decorators import action
from django.utils import timezone
from .services.whatsapp_service import enviar_whatsapp_reserva, enviar_whatsapp_cancelacion




logger = logging.getLogger(__name__)

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated] 

    

# TAMBIEN SE CONFIRMA LA RESERVA Y SE ENVIA LOS DATOS A LA DB Y EL TURNO DISPONIBLE PASA A FALSE
    def perform_create(self, serializer):
        logger.debug(f" Datos validados recibidos: {serializer.validated_data}")
        self.reservar_turno(serializer)

    # def reservar_turno(self, serializer):
    #     try:
    #         user = self.request.user
    #         cliente = Cliente.objects.get(user=user)
    #         turno = serializer.validated_data['turno']

    #         if not turno.disponible:
    #             raise serializers.ValidationError("Este horario ya está reservado")

    #         turno.disponible = False
    #         turno.save()

    #         # reserva = serializer.save(
    #         #     cliente=cliente,
    #         #     sucursal=turno.sucursal
    #         # )
    #         reserva = serializer.save(
    #             cliente=cliente,
    #             sucursal=turno.sucursal,
    #             estado='confirmada'
    #         )

    #         nombre_cliente = cliente.user.get_full_name()

    #         logger.info(f"Reserva creada con éxito ID={reserva.id}")

    #         # MENSAJE WHATSAPP
    #         mensaje_whatsapp = (
    #             f"Hola, soy {nombre_cliente}.\n\n"
    #             f"Reservé un turno:\n"
    #             f"🛠 Servicio: {reserva.servicio.nombre}\n"
    #             f"📅 Fecha: {turno.fecha}\n"
    #             f"⏰ Hora: {turno.hora}\n"
    #             f"📍 Sucursal: {turno.sucursal.nombre}\n\n"
    #             f"Gracias."
    #         )

    #         return Response(
    #             {
    #                 "reserva_id": reserva.id,
    #                 "mensaje_whatsapp": mensaje_whatsapp
    #             },
    #             status=status.HTTP_201_CREATED
    #         )

    #     except Exception as e:
    #         logger.exception(f"Error creando reserva: {str(e)}")
    #         raise

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
                sucursal=turno.sucursal,
                estado='confirmada'
            )

            nombre_cliente = cliente.user.get_full_name() or cliente.user.username
            email = cliente.user.email
            servicio = reserva.servicio.nombre
            precio = f"${reserva.servicio.precio}"
            sucursal = turno.sucursal.nombre
            turno_str = f"{turno.fecha} / {turno.hora}"
            # vehiculo = reserva.vehiculo
            vehiculo = serializer.validated_data['vehiculo']
            vehiculo_texto = f"{vehiculo.marca} {vehiculo.modelo} ({vehiculo.anio_fabricacion})"

            # 🔔 ENVIAR WHATSAPP (notificación interna)
            enviar_whatsapp_reserva(
                nombre_cliente=nombre_cliente,
                email=email,
                servicio=servicio,
                precio=precio,
                sucursal=sucursal,
                turno=turno_str,
                # vehiculo=vehiculo
                vehiculo=vehiculo_texto
            )

            logger.info(f"✅ Reserva creada y WhatsApp enviado ID={reserva.id}")

        except Exception as e:
            logger.exception(f"❌ Error creando reserva: {str(e)}")
            raise


    # ---------- REPROGRAMAR ----------

    @action(detail=True, methods=['post'], url_path='liberar-turno')
    def liberar_turno(self, request, pk=None):
        reserva = self.get_object()

        # si el turno ya paso no se puede reprogramar
        if reserva.turno and reserva.turno.fecha < timezone.now().date():
            return Response(
                {"detail": "El turno ya pasó"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # liberar turno actual
        if reserva.turno:
            reserva.turno.disponible = True
            reserva.turno.save()


        reserva.estado = 'cancelada'
        reserva.save()

        return Response(
            {"detail": "Turno liberado, puede reservar uno nuevo"},
            status=status.HTTP_200_OK
        )

    # ---------- CANCELAR ----------
    @action(detail=True, methods=['put'], url_path='cancelar')
    def cancelar_reserva(self, request, pk=None):
        try:
            reserva = self.get_object()
            cliente = reserva.cliente
            turno = reserva.turno

            # Si ya está cancelada
            if reserva.estado == 'cancelada':
                return Response(
                    {"detail": "La reserva ya está cancelada"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Liberar turno
            if turno:
                turno.disponible = True
                turno.save()

            # Cambiar estado
            reserva.estado = 'cancelada'
            reserva.save()

            # Datos para WhatsApp
            vehiculo = reserva.vehiculo
            vehiculo_texto = f"{vehiculo.marca} {vehiculo.modelo} ({vehiculo.anio_fabricacion})"

            enviar_whatsapp_cancelacion(
                nombre_cliente=cliente.user.get_full_name() or cliente.user.username,
                email=cliente.user.email,
                servicio=reserva.servicio.nombre,
                sucursal=reserva.sucursal.nombre,
                turno=f"{turno.fecha} {turno.hora}",
                vehiculo=vehiculo_texto
            )

            logger.info(f"❌ Reserva cancelada ID={reserva.id}")

            return Response(
                {"detail": "Reserva cancelada correctamente"},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.exception(f"❌ Error cancelando reserva: {str(e)}")
            return Response({"error": str(e)}, status=500)