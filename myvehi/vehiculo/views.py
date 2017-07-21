# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

class VehiculoSerializer(serializers.HyperlinkedModelSerializer):
	empresa = EmpresaLiteSerializer(read_only = True)
	empresa_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Empresa.objects.all())
	class Meta:
		model = SolicitudConsecutivo
		fields = ( 'tipo' ,'placa' ,'ciudad' ,'color' ,'usuario' ,'longitud' ,'lactitud' ,'kilometraje' )

class VehiculoViewSet(viewsets.ModelViewSet):
	"""
	Retorna una lista de informacion , consecutivos  de multas asignados por empresa ,
	puede utilizar el parametro (consecutivo , empresa) a traves del cual, se podra buscar por cada uno de estos filtros
	<br>consecutivo = [numero] <br>
	empresa = [numero].
	"""
	model = Vehiculo
	queryset = model.objects.all()
	serializer_class = VehiculoSerializer

	def retrieve(self,request,*args, **kwargs):
		try:
			instance = self.get_object()
			serializer = self.get_serializer(instance)
			return Response({'message':'','status':'success','data':serializer.data})
		except:
			return Response({'message':'No se encontraron datos','success':'fail','data':''},status=status.HTTP_404_NOT_FOUND)

	def list(self, request, *args, **kwargs):
		try:
			queryset = super(VehiculoViewSet, self).get_queryset()
			consecutivo = self.request.query_params.get('consecutivo', None)
			empresa = self.request.query_params.get('empresa', None)

			qset=(~Q(id=0))

			if consecutivo or empresa:
				if consecutivo:
					qset = qset & ( Q(consecutivo = consecutivo) )					
				if empresa:
					qset =  qset & ( Q(empresa = empresa) )

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
				serializer = VehiculoSerializer(data=request.DATA,context={'request': request})
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


class RequisitoSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = SolicitudConsecutivo
		fields = ( 'nombre' ,'tiene_vencimiento' , 'tiene_soporte' )

class RequisitoViewSet(viewsets.ModelViewSet):
	"""
	Retorna una lista de informacion , paises del mundo ,
	puede utilizar el parametro (dato) a traves del cual, se podra buscar por cada uno de estos filtros
	<br>dato = [letras] <br>
	"""
	model = Requisito
	queryset = model.objects.all()
	serializer_class = RequisitoSerializer

	def retrieve(self,request,*args, **kwargs):
		try:
			instance = self.get_object()
			serializer = self.get_serializer(instance)
			return Response({'message':'','status':'success','data':serializer.data})
		except:
			return Response({'message':'No se encontraron datos','success':'fail','data':''},status=status.HTTP_404_NOT_FOUND)

	def list(self, request, *args, **kwargs):
		try:
			queryset = super(RequisitoViewSet, self).get_queryset()
			dato = self.request.query_params.get('dato', None)
			tieneVencimiento = self.request.query_params.get('tiene_vencimiento', None)
			tieneSoporte = self.request.query_params.get('tiene_soporte', None)

			qset=(~Q(id=0))
			if dato or tieneVencimiento or tieneSoporte:
				if dato:
					qset = qset & ( Q(nombre__icontains = dato) )	
				if tieneVencimiento:
					qset = qset & ( Q(tiene_vencimiento = tieneVencimiento) )
				if tieneSoporte:
					qset = qset & ( Q(tiene_soporte = tieneSoporte) )				

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

class VehiculoRequisitoSerializer(serializers.HyperlinkedModelSerializer):
	empresa = EmpresaLiteSerializer(read_only = True)
	empresa_id = serializers.PrimaryKeyRelatedField(write_only=True,queryset=Empresa.objects.all())
	class Meta:
		model = SolicitudConsecutivo
		fields = ( 'requisito' ,'vehiculo' ,'valor' ,'archivo' )

class VehiculoRequisitoViewSet(viewsets.ModelViewSet):
	"""
	Retorna una lista de informacion , paises del mundo ,
	puede utilizar el parametro (dato) a traves del cual, se podra buscar por cada uno de estos filtros
	<br>dato = [letras] <br>
	"""
	model = VehiculoRequisito
	queryset = model.objects.all()
	serializer_class = VehiculoRequisitoSerializer

	def retrieve(self,request,*args, **kwargs):
		try:
			instance = self.get_object()
			serializer = self.get_serializer(instance)
			return Response({'message':'','status':'success','data':serializer.data})
		except:
			return Response({'message':'No se encontraron datos','success':'fail','data':''},status=status.HTTP_404_NOT_FOUND)

	def list(self, request, *args, **kwargs):
		try:
			queryset = super(VehiculoRequisitoViewSet, self).get_queryset()
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
				serializer = VehiculoRequisitoSerializer(data=request.DATA,context={'request': request})
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
