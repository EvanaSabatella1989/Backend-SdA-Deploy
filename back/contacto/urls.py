from django.urls import path
from .views import enviar_contacto

urlpatterns = [
    path('contacto/', enviar_contacto, name='enviar_contacto'),
]