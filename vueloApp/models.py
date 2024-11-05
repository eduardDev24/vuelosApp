from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Pais(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Aerolinea(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Asiento(models.Model):
    numero = models.CharField(max_length=5)
    disponible = models.BooleanField(default=True)
    precio = models.DecimalField(
        max_digits=10, decimal_places=2, default=80000)

    def __str__(self):
        return self.numero


class Horario(models.Model):
    hora_salida = models.TimeField()
    hora_llegada = models.TimeField()

    def __str__(self):
        return f"{self.hora_salida} - {self.hora_llegada}"


class Boleto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)
    destino_ida = models.ForeignKey(
        Pais, related_name='destino_ida', on_delete=models.CASCADE)
    destino_vuelta = models.ForeignKey(
        Pais, related_name='destino_vuelta', on_delete=models.CASCADE)
    asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    aerolinea = models.ForeignKey(
        Aerolinea, on_delete=models.CASCADE, default=1)
    total_viaje = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Boleto de {self.nombre} - {self.destino_ida} a {self.destino_vuelta}"


class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Mensaje de {self.nombre} ({self.email})'

# -----------------------------------------------------------
