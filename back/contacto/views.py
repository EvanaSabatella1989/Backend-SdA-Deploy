from django.shortcuts import render
from rest_framework import viewsets
from .models import Contacto
from .serializer import ContactoSerializer
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny

class ContactoViewSet(viewsets.ModelViewSet):
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializer
    permission_classes = [AllowAny]  

    def perform_create(self, serializer):
        contacto = serializer.save()

        # datos del mensaje
        nombre = contacto.nombre
        email = contacto.email
        mensaje = contacto.mensaje

        # cuerpo del correo
        cuerpo_email = f"""
        Nuevo mensaje de contacto recibido:

        Nombre: {nombre}
        Email: {email}
        Mensaje:
        {mensaje}
        """

        # envio del correo
        send_mail(
            subject='Nuevo mensaje desde la página de contacto',
            message=cuerpo_email,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.ADMIN_EMAIL], 
            fail_silently=False,
        )
