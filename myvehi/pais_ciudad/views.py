# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import Pais , Ciudad 
# Create your views here.
class PaisSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Pais
		fields = ( 'nombre')

class PaisViewSet(viewsets.ModelViewSet):
	"""
	Retorna una lista de informacion , paises del mundo ,
	puede utilizar el parametro (dato) a traves del cual, se podra buscar por cada uno de estos filtros
	<br>dato = [letras] <br>
	"""
	model = Pais
	queryset = model.objects.all()
	serializer_class = PaisSerializer

	def retrieve(self,request,*args, **kwargs):
		try:
			instance = self.get_object()
			serializer = self.get_serializer(instance)
			return Response({'message':'','status':'success','data':serializer.data})
		except:
			return Response({'message':'No se encontraron datos','success':'fail','data':''},status=status.HTTP_404_NOT_FOUND)

	def list(self, request, *args, **kwargs):
		try:
			queryset = super(PaisViewSet, self).get_queryset()
			dato = self.request.query_params.get('dato', None)

			qset=(~Q(id=0))

			if dato:
				if dato:
					qset = qset & ( Q(nombre__icontains = dato) )					

			queryset = self.model.objects.filter(qset)
	
			#utilizar la variable ignorePagination para quitar la paginacion
			ignorePagination= self.request.query_params.get('ignorePagination',None)
			if ignorePagination is None:
				page = self.paginate_queryset(queryset)
				if page is not None:
					serializer = self.get_serializer(page,many=True)
					return self.get_paginated_response({'message':'','success':'ok','data':serializer.data})

			serializer = self.get_serializer(queryset,many=True)
			return Response({'message':'','success':'ok','data':serializer.data})
		except Exception,e:
			return Response({'message':'Se presentaron errores de comunicacion con el servidor','status':'error','data':''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def create(self, request, *args, **kwargs):
		if request.method == 'POST':
			
			try:
				serializer = PaisSerializer(data=request.DATA,context={'request': request})
				# print serializer
				if serializer.is_valid():
					serializer.save()
					return Response({'message':'El registro ha sido guardado exitosamente','success':'ok',
						'data':serializer.data},status=status.HTTP_201_CREATED)
				else:
					# print serializer.errors
					if "non_field_errors" in serializer.errors:
						mensaje = serializer.errors['non_field_errors']
					elif "nombre" in serializer.errors:
						mensaje = serializer.errors['consecutivo'][0]+" En el campo nombre"
					else: 
						mensaje = 'datos requeridos no fueron recibidos'
				 	return Response({'message': mensaje ,'success':'fail',
			 			'data':''},status=status.HTTP_400_BAD_REQUEST)
			except Exception,e:
				# print e
			 	return Response({'message':'Se presentaron errores al procesar los datos','success':'error', 'data':''},status=status.HTTP_400_BAD_REQUEST)

	def update(self,request,*args,**kwargs):
		if request.method == 'PUT':
			try:
				partial = kwargs.pop('partial', False)
				instance = self.get_object()
				serializer = VehiculoSerializer(instance,data=request.DATA,context={'request': request},partial=partial)
				if serializer.is_valid():
					self.perform_update(serializer)
					return Response({'message':'El registro ha sido actualizado exitosamente','success':'ok',
						'data':serializer.data},status=status.HTTP_201_CREATED)
				else:
				 	return Response({'message':'datos requeridos no fueron recibidos','success':'fail',
			 		'data':''},status=status.HTTP_400_BAD_REQUEST)
			except:
			 	return Response({'message':'Se presentaron errores al procesar los datos','success':'error',
					'data':''},status=status.HTTP_400_BAD_REQUEST)

class CiudadSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Ciudad
		fields = ( 'nombre' ,'pais' ,'pais_id')

class CiudadViewSet(viewsets.ModelViewSet):
	"""
	Retorna una lista de informacion , ciudades de cada pais
	puede utilizar el parametro (dato , pais) a traves del cual, se podra buscar por cada uno de estos filtros
	<br>dato = [letras] <br>
	pais = [numero].
	"""
	model = Ciudad
	queryset = model.objects.all()
	serializer_class = CiudadSerializer

	def retrieve(self,request,*args, **kwargs):
		try:
			instance = self.get_object()
			serializer = self.get_serializer(instance)
			return Response({'message':'','status':'success','data':serializer.data})
		except:
			return Response({'message':'No se encontraron datos','success':'fail','data':''},status=status.HTTP_404_NOT_FOUND)

	def list(self, request, *args, **kwargs):
		try:
			queryset = super(PaisViewSet, self).get_queryset()
			dato = self.request.query_params.get('dato', None)
			paisId = self.request.query_params.get('pais', None)

			qset=(~Q(id=0))

			if dato:
				if dato:
					qset = qset & ( Q(nombre__icontains = dato) )
				if paisId:
					qset = qset & ( Q(pais_id = paisId) )					

			queryset = self.model.objects.filter(qset)
	
			#utilizar la variable ignorePagination para quitar la paginacion
			ignorePagination= self.request.query_params.get('ignorePagination',None)
			if ignorePagination is None:
				page = self.paginate_queryset(queryset)
				if page is not None:
					serializer = self.get_serializer(page,many=True)
					return self.get_paginated_response({'message':'','success':'ok','data':serializer.data})

			serializer = self.get_serializer(queryset,many=True)
			return Response({'message':'','success':'ok','data':serializer.data})
		except Exception,e:
			return Response({'message':'Se presentaron errores de comunicacion con el servidor','status':'error','data':''},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def create(self, request, *args, **kwargs):
		if request.method == 'POST':
			
			try:
				serializer = PaisSerializer(data=request.DATA,context={'request': request})
				print serializer
				if serializer.is_valid():

					sc = SolicitudConsecutivo.objects.filter(empresa_id = request.DATA['empresa_id'])
					
					if sc.count()>0:
						return Response({'message':'La empresa solo puede tener un unico registro','success':'fail',
							'data':serializer.data},status=status.HTTP_400_BAD_REQUEST)
					else:						
						serializer.save(empresa_id =  request.DATA['empresa_id'] )
						return Response({'message':'El registro ha sido guardado exitosamente','success':'ok',
							'data':serializer.data},status=status.HTTP_201_CREATED)
				else:
					# print serializer.errors
					if "non_field_errors" in serializer.errors:
						mensaje = serializer.errors['non_field_errors']
					elif "consecutivo" in serializer.errors:
						mensaje = serializer.errors['consecutivo'][0]+" En el campo consecutivo"
					else: 
						mensaje = 'datos requeridos no fueron recibidos'
				 	return Response({'message': mensaje ,'success':'fail',
			 			'data':''},status=status.HTTP_400_BAD_REQUEST)
			except Exception,e:
				# print e
			 	return Response({'message':'Se presentaron errores al procesar los datos','success':'error', 'data':''},status=status.HTTP_400_BAD_REQUEST)

	def update(self,request,*args,**kwargs):
		if request.method == 'PUT':
			try:
				partial = kwargs.pop('partial', False)
				instance = self.get_object()
				serializer = VehiculoSerializer(instance,data=request.DATA,context={'request': request},partial=partial)
				if serializer.is_valid():
					self.perform_update(serializer)
					return Response({'message':'El registro ha sido actualizado exitosamente','success':'ok',
						'data':serializer.data},status=status.HTTP_201_CREATED)
				else:
				 	return Response({'message':'datos requeridos no fueron recibidos','success':'fail',
			 		'data':''},status=status.HTTP_400_BAD_REQUEST)
			except:
			 	return Response({'message':'Se presentaron errores al procesar los datos','success':'error',
					'data':''},status=status.HTTP_400_BAD_REQUEST)
