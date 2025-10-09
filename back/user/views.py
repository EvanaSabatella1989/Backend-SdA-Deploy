# from django.contrib.auth import authenticate
# from django.contrib.auth import login as rest_framework_login
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken

# from .serializers import UserSerializer

# # Create your views here.


# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)

#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }


# @api_view(['POST'])
# def login(request):
#     email = request.data.get("email", None)
#     password = request.data.get("password", None)
#     user = authenticate(email=email, password=password)
#     print(user)
#     if user:
#         rest_framework_login(request._request, user)
#         token = RefreshToken.for_user(user)
#         token['is_admin'] = user.is_staff

#         # return Response(data={"access_token": str(token.access_token), "refresh_token": str(token), "is_admin": user.is_staff}, status=status.HTTP_200_OK)
        
#         #Modificamos para manejar la sesión de usuario:
#         return Response(data={
#             "access_token": str(token.access_token),
#             "refresh_token": str(token),
#             "is_admin": user.is_staff,
#             "first_name": user.first_name,  # Agregamos el nombre
#             "last_name": user.last_name     # Agregamos el apellido
#         }, status=status.HTTP_200_OK)

#     return Response(data={"message": "No se encontro ningun usuario"}, status=status.HTTP_404_NOT_FOUND)


# @api_view(['POST'])
# def register(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save()
#         return Response(data={"message": "El usuario se registro correctamente"})
#     return Response(status=status.HTTP_404_NOT_FOUND)

from django.contrib.auth import authenticate
from django.contrib.auth import login as rest_framework_login
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from user.models import Cliente
from rest_framework import viewsets
from .serializers import ClienteSerializer
from user.serializers import UserReservaSerializer


from .serializers import UserSerializer

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
@permission_classes([AllowAny])  # Permitir acceso sin autenticación
def login_view(request):
    email = request.data.get("email", None)
    password = request.data.get("password", None)

    if not email or not password:
        return Response({"message": "Email y contraseña son requeridos"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=email, password=password)  # Si usas email como username, cámbialo aquí

    if user:
        rest_framework_login(request._request, user)
        token = get_tokens_for_user(user)

        return Response({
            "access_token": token["access"],
            "refresh_token": token["refresh"],
            "is_admin": user.is_staff,
            "first_name": user.first_name,
            "last_name": user.last_name,
             "id": user.id
            
        }, status=status.HTTP_200_OK)

    return Response({"message": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "El usuario se registró correctamente"}, status=status.HTTP_201_CREATED)
    
    print(serializer.errors)  # 👈 agregá esto
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_perfil(request):
    usuario = request.user  # Obtiene el usuario autenticado
    serializer = UserSerializer(usuario)
    return Response(serializer.data)

# para reserva 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_perfil_reserva(request):
    usuario = request.user
    serializer = UserReservaSerializer(usuario)
    return Response(serializer.data)  


# para obtener los id de los clientes relacionados a usuario
class PerfilClienteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # obtengo el usuario autenticado
        user = request.user

        # obtengo el cliente relacionado con ese usuario
        try:
            cliente = Cliente.objects.get(user=user)
            # retornar el cliente_id relacionado con el usuario
            return Response({
                'cliente_id': cliente.id
            })
        except Cliente.DoesNotExist:
            # si no existe el cliente, retornamos un error
            return Response({'detail': 'Cliente no encontrado'}, status=404)
        
     
#para el admin 
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer      
    
    
