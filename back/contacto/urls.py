from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ContactoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'contacto', ContactoViewSet, basename='contacto')

urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)), 
    # path('contacto/', enviar_contacto, name='enviar_contacto'),
]