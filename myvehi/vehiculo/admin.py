# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Vehiculo, Requisito , VehiculoRequisito
# Register your models here.
class AdminVehiculo(admin.ModelAdmin):
	list_display=('placa', )
	list_filter=('placa', )
	search_fields=('placa',)

class AdminRequisito(admin.ModelAdmin):
	list_display=('nombre',  )
	list_filter=('nombre', )
	search_fields=('nombre',)

class AdminVehiculoRequisito(admin.ModelAdmin):
	list_display=('requisito', 'vehiculo' , 'valor' ,'archivo')
	list_filter=('requisito', )
	search_fields=('requisito',)

admin.site.register( Vehiculo , AdminVehiculo)
admin.site.register( Requisito ,AdminRequisito )
admin.site.register( VehiculoRequisito ,AdminVehiculoRequisito )