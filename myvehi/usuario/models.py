# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
# Create your models here.

class UsuarioApp(models.Model):
	"""Modelo para implementar los usuarios de la aplicacion, utiliza el usuario 
	autenticado de Django pero le agrego una foto"""
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	foto = models.ImageField(upload_to='usuario',blank=True, null=True, default='usuario/default.jpg')
	telefono = models.CharField(max_length=50, blank=True,null=True)
	administraEquipos = models.BooleanField(default=False)
	limiteCantidadEquipos = models.IntegerField(blank=True, null=True,default=0, verbose_name='Limite de equipos')

	def __unicode__(self):
		return self.user.username
	
	def foto_usuario(self):
		  return """<img width="80px" height="80px" src="%s" alt="foto del usuario">""" % self.foto.url

	def nombres(self):
		return self.user.first_name

	def apellidos(self):
		return self.user.last_name

	def correo(self):
		return self.user.email

	foto_usuario.allow_tags=True

	class Meta:		
		db_table = 'Usuario_usuarioApp'
		verbose_name='Usuario de aplicacion'

class ZEquipoTrabajo(models.Model):
	"""Modelo para implementar los equipos de trabajo"""
	nombre = models.CharField(max_length=80)
	administrador = models.ForeignKey(UsuarioApp, on_delete=models.PROTECT, 
		verbose_name='Administrador del equipo', related_name='fk_usurioAdminEquipo')
	usuarios  = models.ManyToManyField(UsuarioApp, related_name='fk_usuariosDelEquipo' , 
		verbose_name='Integrantes del equipo')

	def __unicode__(self):
		return self.nombre

	def nombreAdministrador(self):
		return self.administrador.user.username

	def cantidadIntegrantes(self):
		if ~(self.usuarios is None):			
			return self.usuarios.count()	
		else:
			return 0

	class Meta:		
		db_table = 'Usuario_equipo'
		verbose_name='Equipo'
		unique_together = [
			["nombre"],
		]


