from django.urls import path
from . import views

urlpatterns = [
    path('vehiculo/agregar/', views.agregar_vehiculo, name='agregar_vehiculo'),
    path('vehiculo/<int:pk>/', views.vehiculo_detalle, name='vehiculo_detalle'),  # GET y PUT
    path('vehiculo/eliminar/<int:id>/', views.eliminar_vehiculo, name='eliminar_vehiculo'), # DELETE
]