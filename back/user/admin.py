from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from . import models


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',
                    'is_staff', 'is_superuser', 'is_active', 'last_login', 'is_client')
    list_display_links = ('first_name', 'last_name', 'email', )
    search_fields = ('first_name', 'last_name', 'email',
                     'is_staff', 'is_superuser', 'is_active', 'last_login')
    list_per_page = 25


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_display_links = ('user',)
    search_fields = ('user',)
    list_per_page = 25


class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('cargo',)
    list_display_links = ('cargo',)
    search_fields = ('cargo',)
    list_per_page = 25


admin.site.register(models.UserAccount, CustomUserAdmin)
admin.site.register(models.Cliente, ClienteAdmin)
admin.site.register(models.Empleado, EmpleadoAdmin)
