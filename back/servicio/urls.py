from django.urls import path, include
from rest_framework import routers
from servicio import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ServicioViewSet


router=routers.DefaultRouter()
router.register(r'servicios', ServicioViewSet, basename='servicio')

urlpatterns=[
    path('',include(router.urls)),
    
    # path('api/servicio/<servicio>/',views.servicioList),
    # path('api/servicio/<pk>/',views.servicioList),
    # path('api/servicio/<pk>/update/',views.servicioList),
]
# para que cargue la foto
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)