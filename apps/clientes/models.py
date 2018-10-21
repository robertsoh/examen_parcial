from django.db import models


class ORMCliente(models.Model):
    nombre = models.CharField(max_length=100)


class ORMClienteTelefono(models.Model):
    numero = models.IntegerField()
    cliente = models.ForeignKey(ORMCliente)
    tipo = models.IntegerField()
