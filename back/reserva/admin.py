from django.contrib import admin
from .models import Reserva


class ReservaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'servicio', 'turno', 'servicio', 'estado') 
    list_filter = ('cliente', 'servicio', 'turno', 'servicio', 'estado')
    search_fields = ('cliente', 'servicio', 'turno', 'servicio', 'estado')


admin.site.register(Reserva,ReservaAdmin)

