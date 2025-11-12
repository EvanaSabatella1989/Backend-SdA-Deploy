from django.db import models

# Create your models here.


class Categoria(models.Model):
    TIPO_CHOICES = [
        ("producto", "Producto"),
        ("servicio", "Servicio"),
        ("vehiculo", "Vehiculo"),
    ]

    nombre = models.CharField(max_length=50, blank=False)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default="producto")

    class Meta:
        db_table = "categoria"
        verbose_name_plural = "categorias"
        verbose_name = "categoria"

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"
