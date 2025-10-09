from django.urls import path
from .views import obtener_carrito, agregar_al_carrito, eliminar_del_carrito, modificar_cantidad_carrito, vaciar_carrito

urlpatterns = [
    path('carrito/', obtener_carrito, name='obtener_carrito'),
    path('carrito/agregar/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/modificar/', modificar_cantidad_carrito, name='modificar_cantidad_carrito'),
    # path('carrito/eliminar/<int:item_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/eliminar/<int:producto_id>/', eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/vaciar_carrito/', vaciar_carrito, name='vaciar_carrito')
    
]