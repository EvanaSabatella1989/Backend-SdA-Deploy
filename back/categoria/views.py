# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework import viewsets,generics,request,status
# from .serializer import CategoriaSerializer
# from .models import Categoria
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny



# class CategoriaViewSet(viewsets.ModelViewSet):
#     queryset=Categoria.objects.all()
#     serializer_class=CategoriaSerializer


# # elimina
# class CategoriaUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
#     queryset=Categoria.objects.all()
#     serializer_class=CategoriaSerializer


# @csrf_exempt   #trae y crea categorias
# @permission_classes([AllowAny])  # Esto hace que la vista sea pública
# @api_view(['GET', 'POST', 'PUT', 'DELETE'])
# def categoriaList(request, format=None):
#     '''
#     List all code snippets, or create a new snippet.
#     Enumere todos los fragmentos de código o cree uno nuevo.
#     '''
#     if request.method == 'GET':
#         categoria = Categoria.objects.all()
#         serializer = CategoriaSerializer(categoria, many=True)
       
#         return Response(serializer.data)

#     elif request.method == 'POST':
        
#         serializer = CategoriaSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # print('desde create'+serializer)
           
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
  
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'PUT':
#         serializer = CategoriaSerializer(categoria, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # print('desde create'+serializer)
           
#             return Response(serializer.data)
  
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         categoria.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializer import CategoriaSerializer
from .models import Categoria
from rest_framework import status
from rest_framework.response import Response


class CategoriaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para listar, crear, actualizar y eliminar categorías.
    Soporta filtro por tipo con ?tipo=producto o ?tipo=servicio
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]  # público, podés ajustarlo luego

    def get_queryset(self):
        queryset = super().get_queryset()
        tipo = self.request.query_params.get("tipo")  # filtrar por tipo
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        return queryset

    def destroy(self, request, *args, **kwargs):
        categoria = self.get_object()

        # 🔍 Verificar si tiene productos o servicios asociados
        tiene_productos = hasattr(categoria, 'productos') and categoria.productos.exists()
        tiene_servicios = hasattr(categoria, 'servicios') and categoria.servicios.exists()

        if tiene_productos or tiene_servicios:
            return Response(
                {"error": "No se puede eliminar la categoría porque tiene productos o servicios asociados."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Si no tiene relaciones, se elimina normalmente
        categoria.delete()
        return Response(
            {"mensaje": "Categoría eliminada correctamente."},
            status=status.HTTP_204_NO_CONTENT
        )


    

        
