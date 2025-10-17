from django.shortcuts import render
from rest_framework import viewsets,generics,status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializer import ProductoSerializer
from .models import Producto
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes, parser_classes
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser ,FormParser

class ProductoViewSet(viewsets.ModelViewSet):
    queryset=Producto.objects.all()
    serializer_class=ProductoSerializer

class ProductoUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset=Producto.objects.all()
    serializer_class=ProductoSerializer

@csrf_exempt   
# @permission_classes([AllowAny])  # Esto hace que la vista sea pública
@api_view(['GET', 'POST','PUT','DELETE'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])  # 👈 esta línea es CLAVE
def productoList(request, format=None):
    parser_classes = (MultiPartParser, FormParser)  # ✅ habilitar multipart
    '''
    List all code snippets, or create a new snippet.
    Enumere todos los fragmentos de código o cree uno nuevo.
    '''
    if request.method == 'GET':
        producto = Producto.objects.all()
        serializer = ProductoSerializer(producto, many=True)
        # return JsonResponse(serializer.data, safe=False)
        return Response(serializer.data)


    elif request.method == 'POST':
        
        # data = JSONParser().parse(request)    
        # data.imagen=request.FILES.get('imagen')
        # serializer = SnippetSerializer(data=data)     #1
        print("🧩 Datos recibidos:", request.data)
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        if not request.user.is_staff:
            return Response({'detail': 'No tiene permiso para realizar esta acción.'}, 
                            status=status.HTTP_403_FORBIDDEN)

        try:
            producto = Producto.objects.get(pk=request.data.get('id'))
        except Producto.DoesNotExist:
            return Response({'detail': 'Producto no encontrado.'}, 
                            status=status.HTTP_404_NOT_FOUND)

        old_public_id = producto.public_id  # public_id anterior

        data = request.data.copy()
        serializer = ProductoSerializer(producto, data=data, partial=True)

        if serializer.is_valid():
            # Si hay nueva imagen y existe una anterior
            if 'imagen' in request.FILES and old_public_id:
                import cloudinary.uploader

                # Asegurarse de pasar solo el public_id correcto
                # Por ejemplo, si guardaste "tapizado" en public_id, así está correcto
                try:
                    cloudinary.uploader.destroy(old_public_id, invalidate=True)
                except Exception as e:
                    print(f"No se pudo borrar la imagen anterior: {e}")

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




  
    elif request.method == 'DELETE':
       # Verifica si el usuario es admin
        if not request.user.is_staff:
            return Response({'detail': 'No tiene permiso para realizar esta acción.'}, 
                            status=status.HTTP_403_FORBIDDEN)

        try:
            producto = Producto.objects.get(pk=request.data.get('id'))
        except Producto.DoesNotExist:
            return Response({'detail': 'Producto no encontrado.'}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        #  # ✅ Eliminar imagen de Cloudinary si tiene public_id
        # if producto.public_id:
        #     try:
        #         cloudinary.uploader.destroy(producto.public_id)
        #     except Exception as e:
        #         print("Error eliminando en Cloudinary:", e)

        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
