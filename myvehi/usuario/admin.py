# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import UsuarioApp, ZEquipoTrabajo
# Register your models here.

class AdminUsuarioApp(admin.ModelAdmin):
	list_display=('user','nombres','apellidos','correo','foto_usuario','administraEquipos','limiteCantidadEquipos')
	list_filter=('administraEquipos',)
	search_fields=('user__username','user__first_name','user__last_name','user__email',)	

class AdminZEquipoTrabajo(admin.ModelAdmin):
	list_display = ('nombre','nombreAdministrador','cantidadIntegrantes')
	search_fields=('nombre',)


admin.site.register(UsuarioApp,AdminUsuarioApp)
admin.site.register(ZEquipoTrabajo,AdminZEquipoTrabajo)
