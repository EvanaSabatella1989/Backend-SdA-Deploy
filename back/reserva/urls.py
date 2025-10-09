from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservaViewSet



router = DefaultRouter()
router.register(r"reservas", ReservaViewSet,basename='reservas')

urlpatterns = [
    
    path('', include(router.urls)), 
    # path('reservar-turno/', reservar_turno, name='reservar_turno'),
    # path('eliminar-turno/<int:reserva_id>/',eliminar_turno,name='eliminar_turno'),
]