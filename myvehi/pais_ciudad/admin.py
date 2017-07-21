# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import Pais, Ciudad

# Register your models here.
class AdminPais(admin.ModelAdmin):
	list_display=('nombre', )
	list_filter=('nombre', )
	search_fields=('nombre',)

class AdminCiudad(admin.ModelAdmin):
	list_display=('nombre', 'pais' )
	list_filter=('pais', )
	search_fields=('nombre',)

admin.site.register(Pais, AdminPais)
admin.site.register(Ciudad, AdminCiudad)
