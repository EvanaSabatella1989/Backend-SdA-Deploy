from django.db import models
from categoria.models import Categoria
from datetime import datetime
import re
import cloudinary.uploader
from urllib.parse import urlparse
import os

# Create your models here.




class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    # imagen = models.ImageField(upload_to='photos/')
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True) # Cloudinary maneja el upload
    public_id = models.CharField(max_length=255, blank=True, null=True)       # ✅ nuevo campo
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="productos")
    cantidad = models.IntegerField(default=0)
    date_created = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = "producto"
        verbose_name_plural = "productos"
        verbose_name = "producto"

    def get_thumbnail(self):
        if self.imagen:
            return self.imagen.url
        return 'imagen.url'

    # def get_absolute_image_url(self):
    #     if self.imagen:
    #         return f"{settings.MEDIA_URL}{self.imagen}"
    #     return ""

    def save(self, *args, **kwargs):
        # ✅ Si el producto ya existe en la BD, buscamos la versión anterior
        if self.pk:
            try:
                old = type(self).objects.get(pk=self.pk)
                # Si el public_id existe y la imagen cambió → borrar de Cloudinary
                if old.public_id and old.imagen != self.imagen:
                    try:
                        cloudinary.uploader.destroy(old.public_id)
                    except Exception as e:
                        print(f"Error al eliminar imagen anterior en Cloudinary: {e}")
            except type(self).DoesNotExist:
                pass  # Si no existía antes, seguimos normal

        # ✅ Guardamos primero
        super().save(*args, **kwargs)

        # ✅ Luego calculamos el nuevo public_id
        if self.imagen:
            try:
                url = str(self.imagen.url)
                path = urlparse(url).path
                filename = os.path.basename(path).rstrip('/')
                public_id_candidate = filename

                if public_id_candidate and public_id_candidate != self.public_id:
                    final_public_id = "media/productos/" + public_id_candidate
                    self.public_id = final_public_id
                    type(self).objects.filter(pk=self.pk).update(public_id=final_public_id)
            except Exception as e:
                print("Error extrayendo public_id:", e)


   
    def delete(self, *args, **kwargs):
        if self.public_id:
            try:
                cloudinary.uploader.destroy(self.public_id)
            except Exception as e:
                print(f"Error al eliminar imagen en Cloudinary: {e}")
        super().delete(*args, **kwargs)            

    def __str__(self):
        return self.nombre
