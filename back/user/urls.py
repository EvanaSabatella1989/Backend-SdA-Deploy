# from django.urls import path
# from . import views

# urlpatterns = [
#     path('registro/', views.register),
#     path('login/', views.login)
# ]

from django.urls import path,include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import obtener_perfil,PerfilClienteView,obtener_perfil_reserva
from .views import ClienteViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)

urlpatterns = [
    path('registro/', views.register),
    path('login/', views.login_view),  # Cambiamos el nombre a login_view
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('perfil/', obtener_perfil, name='obtener_perfil'),
    path('perfil-cliente/', PerfilClienteView.as_view(), name='perfil-cliente'),
    path('', include(router.urls)),
    path('perfil-reserva/',obtener_perfil_reserva, name='obtener_perfil_reserva'),
]