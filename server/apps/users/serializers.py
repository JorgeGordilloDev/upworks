from rest_framework.serializers import Serializer, ModelSerializer, CharField, ValidationError
from rest_framework.fields import CharField
from .models import User, Role


class RoleSerializer(ModelSerializer):
	class Meta:
		model = Role
		fields = ('name',)
	
	def to_representation(self, instance:Role):
		return instance.name


class UserSerializer(ModelSerializer):

	def to_representation(self, instance:User):
		roles = RoleSerializer(many=True, read_only=True, instance=instance.roles)
		return {
			'id': instance.pk,
			'email': instance.email,
			'roles': roles.data
		}

	def create(self, validated_data):
		user = User(**validated_data)
		user.set_password(validated_data['password'])
		user.save()
		return user

	class Meta:
		model = User
		fields = ('id', 'email', 'roles')
	

class UserUpdateSerializer(ModelSerializer):

	class Meta:
		model = User
		fields = ('email',)


class PasswordSerializer(Serializer):
	password = CharField(max_length=128, min_length=6, write_only=True)
	password2 = CharField(max_length=128, min_length=6, write_only=True)

	def validate(self, data):
		if data['password'] != data['password2']:
			raise ValidationError(
				{ 'password': 'La contraseña no son iguales' }
			)
		return data