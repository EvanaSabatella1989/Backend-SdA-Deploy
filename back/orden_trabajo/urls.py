from rest_framework.routers import DefaultRouter

from orden_trabajo.views import OrdenTrabajoViewSet

router = DefaultRouter()

router.register(r"ordenes_trabajo", OrdenTrabajoViewSet, basename='orden_trabajo')

urlpatterns = router.urls