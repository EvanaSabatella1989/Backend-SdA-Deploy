from django.contrib import admin
from .models import Contacto

class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre','email','mensaje','fecha_envio')
    list_display_links =   ('nombre','email','mensaje','fecha_envio')
    search_fields =  ('nombre','email','mensaje','fecha_envio')
    list_per_page = 25


admin.site.register(Contacto,ContactoAdmin)


