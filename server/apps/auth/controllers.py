from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import TokenObtainPairSerializer, UserCustomSerializer


class Login(TokenObtainPairView):
	serializer_class = TokenObtainPairSerializer

	def post(self, request, *args, **kwargs):
		email = request.data.get('email', '')
		password = request.data.get('password', '')
		user = authenticate(
			email=email,
			password=password
		)

		if user:
			login_serializer = self.serializer_class(data=request.data)
			if login_serializer.is_valid():
				user_serializer = UserCustomSerializer(user)
				data =  {
					'access': login_serializer.validated_data.get('access'),
					'refresh': login_serializer.validated_data.get('refresh'),
					**user_serializer.data,
				}
				
				return Response(data, status=201)
			return Response({ 'error': 'Correo o contraseña incorrectos' }, status=400)
		return Response({ 'error': 'Correo o contraseña incorrectos' }, status=400)
