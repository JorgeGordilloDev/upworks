from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import Serializer, ValidationError, ModelSerializer
from rest_framework.fields import CharField
from apps.users.models import User, Role
from apps.users.serializers import RoleSerializer

class TokenSerializer(TokenObtainPairSerializer):
	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)

		# add custom claims
		token['roles'] = user.roles
		return token


class UserCustomSerializer(ModelSerializer):
	roles = RoleSerializer(many=True, read_only=True)

	class Meta:
		model = User
		fields = ('id', 'email', 'roles')


class PasswordSerializer(Serializer):
	password = CharField(max_length=128, min_length=6, write_only=True)
	password2 = CharField(max_length=128, min_length=6, write_only=True)

	def validate(self, attrs):
		if attrs['password'] != attrs['password2']:
			raise ValidationError(
				{ 'password': 'La contraseña no son iguales' }
			)