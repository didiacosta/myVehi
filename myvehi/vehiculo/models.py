# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from pais_ciudad.models import Ciudad

# Create your models here.
class BaseModel(models.Model):
 nombre = models.CharField(max_length=250)

 class Meta:
   abstract = True

 def __unicode__(self):
  return self.nombre


class Vehiculo(models.Model):
	tipo = models.BigIntegerField()
	placa = models.CharField(max_length=10)
	ciudad = models.ForeignKey(Ciudad , related_name = 'fk_Ciudad_Vehiculo' , on_delete=models.PROTECT)
	color = models.CharField(max_length=50)
	usuario = models.BigIntegerField()
	longitud = models.CharField(max_length=50)
	lactitud = models.CharField(max_length=50)
	kilometraje = models.BigIntegerField()

class Requisito(BaseModel):
	tiene_vencimiento = models.BooleanField(default=False)
	tiene_soporte = models.BooleanField(default=False)

class VehiculoRequisito(BaseModel):
	requisito = models.ForeignKey(Requisito , related_name = 'fk_Requisito_VehiculoRequisito' , on_delete=models.PROTECT)
	vehiculo = models.ForeignKey(Vehiculo , related_name = 'fk_Vehiculo_VehiculoRequisito' , on_delete=models.PROTECT)
	valor = models.CharField(max_length=50)
	archivo = models.CharField(max_length=50)