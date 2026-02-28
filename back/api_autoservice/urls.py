from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from servicio.models import Servicio
from reserva.models import Reserva
from servicio.serializer import ServicioSerializer
from servicio import views
# from categoria.views import CategoriaUpdateDelete, categoriaList
from categoria.views import CategoriaViewSet
from carrito.views import Carrito
from vehiculo.views import Vehiculo
from orden_trabajo.models import OrdenTrabajo
from rest_framework import routers

router = routers.DefaultRouter()
# router.register(r'servicio', views.ServicioViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user.urls')),
    path('api/', include('servicio.urls')),
    path('api/', include('producto.urls')),
    path('api/', include('venta.urls')),
    path('api/', include('reserva.urls')),
    path('api/', include('sucursal.urls')),

    path('api/',include('contacto.urls')),
    # path('api/servicio/servicioList/',views.servicioList),
    # path('api/servicio/delete/<pk>/', ServicioUpdateDelete.as_view()),
    # path('api/', include('categoria.urls')),
    # path('api/categoria/<pk>/', categoriaList),
    # path('api/categoria/update/<pk>/', categoriaList),
    # path('api/categoria/', categoriaList),
    # path('api/categoria/detail/<pk>/', categoriaList),
    path('api/', include('categoria.urls')),
    path('api/',include('turno.urls')),
    path('api/', include('carrito.urls')),
    path('api/', include('vehiculo.urls')),
    path('api/', include('orden_trabajo.urls'))
]
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# para que cargue la foto
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
