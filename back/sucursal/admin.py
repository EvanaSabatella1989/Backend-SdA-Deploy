from django.contrib import admin
from .models import Sucursal
# Register your models here.


class SucursalAdmin(admin.ModelAdmin):
    list_display = ('direccion', 'nombre')
    list_display_links = ('direccion', 'nombre')
    search_fields = ('direccion', 'nombre')
    list_per_page = 25


# class HorarioSucursalAdmin(admin.ModelAdmin):
#     list_display = ('sucursal','fecha','hora','disponible')
#     list_display_links =('sucursal','fecha','hora','disponible')
#     search_fields =('sucursal','fecha','hora','disponible')
#     list_per_page = 25




admin.site.register(Sucursal, SucursalAdmin)
# admin.site.register(HorarioSucursal)
