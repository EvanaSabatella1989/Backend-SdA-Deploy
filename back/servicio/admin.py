from django.contrib import admin
from .models import Servicio
# Register your models here.


class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'imagen', 'precio', 'descripcion')
    list_display_links = ('nombre', 'imagen', 'precio',
                          'descripcion')
    search_fields = ('nombre', 'imagen', 'precio',
                     'descripcion')
    list_per_page = 25


admin.site.register(Servicio, ServicioAdmin)
