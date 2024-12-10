from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=20, verbose_name="RUT")
    email = models.EmailField(verbose_name="Correo electrónico")
    descripcion = models.TextField(verbose_name="Descripción")
    evidencia = models.ImageField(upload_to='evidencias/', verbose_name="Evidencia (JPG)")
    latitud = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Latitud")
    longitud = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Longitud")
    fecha = models.DateField(default=now, verbose_name="Fecha")
    hora = models.TimeField(default=now, verbose_name="Hora")
    dias_transcurridos = models.IntegerField(default=0, verbose_name="Días transcurridos")
    estado = models.CharField(max_length=50,
        choices=[
            ('Pendiente', 'Pendiente'),
            ('En Proceso', 'En Proceso'),
            ('Completada', 'Completada'),
        ],
        default='Pendiente',
        verbose_name="Estado",
    )

    def __str__(self):
        return f"Task: {self.user} - {self.estado}"
