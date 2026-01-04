from django.urls import path, include
from rest_framework import routers
from .views import ReferenceMPView, ConfirmarPagoView,VentaDetailView,VentaListView


urlpatterns = [
    path('venta/preference/', ReferenceMPView.as_view()),
    path('venta/confirmar-pago/', ConfirmarPagoView.as_view(), name='confirmar-pago'),
    path('ventas/', VentaListView.as_view(), name='ventas'),
    path('ventas/<int:pk>/', VentaDetailView.as_view(), name='venta-detalle'),
]


