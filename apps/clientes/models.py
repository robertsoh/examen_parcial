from django.db import models


class ORMCliente(models.Model):
    nombre = models.CharField(max_length=100)
