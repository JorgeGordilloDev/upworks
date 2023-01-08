from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """Allows access only to authenticated users."""

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and 3 in request.user.roles)


class IsRecluterUser(BasePermission):
	def has_permission(self, request, view):
		return bool(request.user.is_authenticated and 2 in request.user.roles)


class IsEmployeeUser(BasePermission):
	def has_permission(self, request, view):
		return bool(request.user.is_authenticated and 1 in request.user.roles)