from django.db import models

class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    mensaje = models.CharField(max_length=255)
    fecha_envio = models.DateTimeField(auto_now_add=True)


class Meta:
    db_table = "contacto"
    verbose_name_plural = "contactos"
    verbose_name = "contacto"


    def __str__(self):   
        return f"Mensaje de contacto enviado por {self.nombre}. Su correo es {self.email}"