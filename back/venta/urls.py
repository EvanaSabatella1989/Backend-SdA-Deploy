from django.urls import path, include
from rest_framework import routers
from .views import ReferenceMPView, ConfirmarPagoView


urlpatterns = [
    path('preference', ReferenceMPView.as_view()),
    path("confirmar-pago", ConfirmarPagoView.as_view(), name="confirmar-pago"),
]
