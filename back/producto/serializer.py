from rest_framework import serializers
from django.conf import settings
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    # imagen = serializers.SerializerMethodField()

    # def get_imagen(self, obj):
    #     request = self.context.get('request')
    #     if obj.imagen:
    #         return request.build_absolute_uri(obj.imagen.url) if request else f"{settings.MEDIA_URL}{obj.imagen}"
    #     return ""

    class Meta:
        model=Producto
        fields='__all__' #,['nombre','imagen','descripcion','precio','categoria','cantidad','date_created']
        extra_kwargs = {
            'imagen': {'required': False, 'allow_null': True}
        }
        depth = 1