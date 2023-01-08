from django.shortcuts import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import User
from .serializers import UserSerializer, UserUpdateSerializer, PasswordSerializer
from .filters import UserFilter


class UserController(GenericViewSet):
	model = User
	serializer_class = UserSerializer
	update_serializer_class = UserUpdateSerializer
	password_serializer_class = PasswordSerializer
	serializers = {
		'default': UserSerializer,
		'update': UserUpdateSerializer,
		'password': PasswordSerializer
	}
	filterset_class = UserFilter
	filterset_fields = ['email',]

	def get_queryset(self):
		return self.model.objects.order_by('-id')
	
	def get_object(self, pk):
		return get_object_or_404(self.model, pk=pk)
	
	def get_serializer_class(self):
		return self.serializers.get(self.action, self.serializers['default'])
	
	def get_context_data(self, **kwars):
		context = super().get_context_data(**kwars)
		context['filter'] = self.filterset_class(self.request.GET, queryset=self.get_queryset())
		return context
	
	def retrieve(self, request, pk):
		data = self.get_object(pk)
		serializer = self.serializer_class(data)
		return Response(serializer.data)
	
	def list (self, request):
		queryset = self.filter_queryset(self.get_queryset())
		page = self.paginate_queryset(queryset)

		serializer = self.get_serializer(page, many=True)
		return self.get_paginated_response(serializer.data)
	
	def create(self, request):
		serializer = self.serializer_class(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response({
				'message': 'Usuario creado correctamente',
				'data': serializer.data
			}, status=201)

		return Response({
			'error': 'Se produjo un error al crear el usuario',
			'errors': serializer.errors
		}, status=400)
	
	@action(detail=True, methods=['post'], url_path='password')
	def password(self, request, pk=None):
		user = self.get_object(pk)
		serializer = self.password_serializer_class(data=request.data)
		if serializer.is_valid():
			user.set_password(serializer.validated_data['password'])
			user.save()
			return Response({
				'message': 'Contraseña actualizada correctamente'
			})
		return Response({
			'message': 'Hay errores en la información enviada',
			'errors': serializer.errors
		}, status=400)
	
	def update(self, request, pk):
		user = self.get_object(pk)
		serializer = self.update_serializer_class(user, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({
				'message': 'Usuario actualizado correctamente',
				'data': serializer.data
			}, status=200)
		
		return Response({
			'error': 'Se produjo un error al actualizar los datos',
			'erros': serializer.errors
		}, status=200)
	
	def destroy(self, request, pk):
		data = self.get_object(pk)
		try:
			data.is_active = False
			data.save()
			return Response({
				'message': 'Registro eliminado correctamente'
			}, status=204)
		except:
			return Response({
				'error': 'Error al eliminar el usuario'
			}, status=400)
	
	def partial_update(self, request, pk=None):
		pass