from django.contrib import admin
from .models import Turno
# Register your models here.


class TurnoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'hora')
    list_display_links = ('fecha', 'hora')
    search_fields = ('fecha', 'hora', 'sucursal')
    list_per_page = 25


admin.site.register(Turno, TurnoAdmin)
