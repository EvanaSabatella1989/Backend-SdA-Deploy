from django.shortcuts import render
from rest_framework import viewsets
from .models import Contacto
from .serializer import ContactoSerializer
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status

class ContactoViewSet(viewsets.ModelViewSet):
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializer



@api_view(['POST'])
def enviar_contacto(request):
    serializer = ContactoSerializer(data=request.data)
    if serializer.is_valid():
        # guardar en la base de datos
        contacto = serializer.save()
        # enviar correo al admin
        asunto = "Nuevo mensaje de contacto"
        mensaje = f"""
        Nombre: {contacto.nombre}
        Email: {contacto.email}
        Mensaje: {contacto.mensaje}
        """
        send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, ['admin@tuempresa.com'])

        return Response({"mensaje": "Formulario enviado con éxito"}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
