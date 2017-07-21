# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class BaseModel(models.Model):
 nombre = models.CharField(max_length=250)

 class Meta:
   abstract = True

 def __unicode__(self):
  return self.nombre


class Pais(BaseModel):
	class Meta:
		unique_together = (("nombre"),)

class Ciudad(BaseModel):
	pais = models.ForeignKey(Pais , related_name = 'fk_Pais_Ciudad' , on_delete=models.PROTECT)
	class Meta:
		unique_together = (("nombre" ,"pais"),)
	