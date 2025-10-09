from django.db import models
from datetime import datetime
from categoria.models import Categoria
from cloudinary_storage.storage import MediaCloudinaryStorage
import os
from urllib.parse import urlparse
import cloudinary.uploader




class Servicio(models.Model):
    id=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="servicios",null=True, blank=True)
    imagen = models.ImageField(storage=MediaCloudinaryStorage(), upload_to='servicios/', blank=True, null=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion= models.DateTimeField(default=datetime.now)
    public_id = models.CharField(max_length=255, blank=True, null=True)
    # sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="servicios",null=True, blank=True)

    class Meta:
        db_table = "servicio"
        verbose_name_plural = "servicios"
        verbose_name = "servicio"

    def get_thumbnail(self):
        if self.imagen:
            return self.imagen.url
        return 'imagen.url'

    def __str__(self):
        return self.nombre


    def save(self, *args, **kwargs):
        # si el servicio ya existe en la BD buscamos la versión anterior
        if self.pk:
            try:
                old = type(self).objects.get(pk=self.pk)
                # Si el public_id existe y la imagen cambió  borrar de Cloudinary
                if old.public_id and old.imagen != self.imagen:
                    try:
                        cloudinary.uploader.destroy(old.public_id)
                    except Exception as e:
                        print(f"Error al eliminar imagen anterior en Cloudinary: {e}")
            except type(self).DoesNotExist:
                pass  # Si no existía antes seguimos normal

        # Guardamos primero
        super().save(*args, **kwargs)

        # Luego calculamos el nuevo public_id
        if self.imagen:
            try:
                url = str(self.imagen.url)
                path = urlparse(url).path
                filename = os.path.basename(path).rstrip('/')
                public_id_candidate = filename

                if public_id_candidate and public_id_candidate != self.public_id:
                    final_public_id = "media/servicios/" + public_id_candidate
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

