from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets,generics,request,status
from .serializer import ServicioSerializer
from .models import Servicio
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from servicio.serializer import ServicioConSucursalesSerializer
from rest_framework.decorators import action

class ServicioViewSet(viewsets.ModelViewSet):
    queryset=Servicio.objects.all()
    serializer_class=ServicioSerializer
    parser_classes=(MultiPartParser, FormParser,JSONParser)

    @permission_classes([AllowAny])  
    def list(self,request):
        # lista todos los servicios
        servicios=self.get_queryset()
        serializer=self.get_serializer(servicios,many=True)
        return Response(serializer.data)

    @permission_classes([AllowAny])  
    def detail(self,request,pk=None):
        # SOLO UN SERVICIO
        try:
            servicio=self.get_queryset().get(pk=pk)
            serializer=self.get_serializer(servicio)
            return Response(serializer.data)
        except Servicio.DoesNotExist:
            return Response({'error','servicio no encontrado'},status=status.HTTP_404_NOT_FOUND)
        
    @permission_classes([AllowAny])  
    def create(self, request):
        # crea un nuevo servicio
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    @permission_classes([AllowAny])  
    def update(self, request, pk=None):
        """Actualizar un servicio"""
        try:
            servicio = self.get_queryset().get(pk=pk)
            data = request.data.copy()  

            if 'imagen' not in data or data['imagen'] == 'null':
                data.pop('imagen', None)  

            serializer = self.get_serializer(servicio, data=data, partial=True)  


            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Servicio.DoesNotExist:
            return Response({"error": "Servicio no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    @permission_classes([AllowAny])     
    def destroy(self, request, pk=None):
        """Eliminar un servicio"""
        try:
            servicio = self.get_queryset().get(pk=pk)
            servicio.delete()
            return Response({"message": "Servicio eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)
        except Servicio.DoesNotExist:
            return Response({"error": "Servicio no encontrado"}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=False, methods=['get'], url_path='con-sucursales')
    @permission_classes([AllowAny])
    def con_sucursales(self, request):
        servicios = self.get_queryset()
        serializer = ServicioConSucursalesSerializer(servicios, many=True)
        return Response(serializer.data)

