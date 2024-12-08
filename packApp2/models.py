from django.db import models


# Create your models here.


class Pack_promocion(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    estadias = models.CharField(max_length=100)
    transporte = models.CharField(max_length=100)
    comidas = models.CharField(max_length=100)
    hoteles = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id) + " " +self.nombre + " " + self.destino + " " +self.estadias + " " +self.transporte + " " +self.comidas + " " +self.hoteles + "($" + str(self.precio) + ")"






