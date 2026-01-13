from django.urls import path, include
from rest_framework import routers
from producto import views


router=routers.DefaultRouter()
router.register(r'producto',views.ProductoViewSet)

# urlpatterns=[
#     path('',include(router.urls)),
#     path('api/producto/<servicio>/',views.productoList),
#     path('api/producto/<pk>/',views.productoList),
# ]

urlpatterns = [
    path('productos/', views.productoList),                 # GET (listar) / POST (crear)
    path('producto/<int:pk>/', views.productoDetail),     # GET / PUT / DELETE
]
