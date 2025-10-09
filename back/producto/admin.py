from django.contrib import admin
from .models import Producto
# Register your models here.


class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'imagen', 'precio', 'descripcion', 'cantidad')
    list_display_links = ('nombre', 'imagen', 'precio',
                          'descripcion', 'cantidad')
    search_fields = ('nombre', 'imagen', 'precio',
                     'descripcion', 'cantidad', 'categoria')
    list_per_page = 25


admin.site.register(Producto, ProductoAdmin)
