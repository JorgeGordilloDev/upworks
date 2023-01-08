from django_filters.rest_framework import FilterSet
from .models import User


class UserFilter(FilterSet):
	class Meta:
		model = User
		fields = ['is_active', 'roles', 'is_staff']