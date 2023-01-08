from django.contrib import auth
from django.db.models import Model, CharField, EmailField, DateTimeField, BooleanField, ManyToManyField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from simple_history.models import HistoricalRecords


# --- Rol de Usuario - Model --- #
class Role(Model):
	name = CharField('Nombre', max_length=15, )
	description = CharField(max_length=30, verbose_name='Descripción')

	def __str__(self): 
		return self.name
	
	class Meta:
		db_table = 'UPWORKS_ROLES_CAT'
		managed = True
		verbose_name = 'Rol'
		verbose_name_plural = 'Roles'


# --- Administrador de Usuarios --- #
class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		"""Cree y guarde un usuario con el usuario, el email y la contraseña proporcionados."""
		if not email:
			raise ValueError("El correo es obligatorio")

		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault("is_staff", False)
		extra_fields.setdefault("is_superuser", False)
		
		user = self._create_user(email, password, **extra_fields)
		user.roles.add(Role.objects.get(id=1))
		return user
	
	def create_superuser(self, email, password=None, **extra_fields):
		extra_fields.setdefault("is_staff", True)
		extra_fields.setdefault("is_superuser", True)

		user = self._create_user(email, password, **extra_fields)
		user.roles.add(Role.objects.get(id=3))
		return user
	
	def with_perm(
		self, perm, is_active=True, include_superusers=True, backend=None, obj=None
	):
		if backend is None:
			backends = auth._get_backends(return_tuples=True)
			if len(backends) == 1:
				backend, _ = backends[0]
			else:
				raise ValueError(
					"Tiene varios backends de autenticación configurados y "
					"por lo tanto, debe proporcionar el argumento `backend`"
				)
		elif not isinstance(backend, str):
			raise TypeError(
				"backend debe ser una cadena de ruta de importación con puntos (got %r)." % backend
			)
		else:
			backend = auth.load_backend(backend)
		if hasattr(backend, "with_perm"):
			return backend.with_perm(
				perm,
				is_active=is_active,
				include_superusers=include_superusers,
				obj=obj,
			)
		return self.none()


# --- Usuarios - Model --- #
class User(AbstractBaseUser, PermissionsMixin):
	"""
	Los usuarios dentro del sistema de autenticación están representados por este modelo.

	Se requiere nombre de usuario, email y  contraseña. Otros campos son opcionales.
	"""

	# Credentials
	email = EmailField('Email',
		max_length=254,
		unique=True,
		null=False,
		blank=False,
		help_text="Obligatorio. Correo electronico.",
		error_messages={
			"unique": "Ya existe un usuario con este email.",
		},
	)

	# Permissions
	roles = ManyToManyField(Role, 
		verbose_name='Rol',
		help_text='Designa los roles que tendra el usuario',
		blank=True,
	)
	is_staff = BooleanField(
		"Es staff",
		default=False,
		help_text="Designa si el usuario puede iniciar sesión en este sitio de administración",
	)
	is_active = BooleanField(
		"Es activo",
		default=True,
		help_text=
			"Designa si este usuario debe ser tratado como activo."
			"Desmarcar esto en lugar de eliminar cuentas"
	)

	# Metadata
	joined_at = DateTimeField("Fecha de registro", 
		auto_now=False, 
		auto_now_add=True, 
		editable=False
	)
	update_at = DateTimeField("Ultima modificacion", 
		auto_now=True, 
		auto_now_add=False
	)
	historical = HistoricalRecords()
	objects = UserManager()

	EMAIL_FIELD = "email"
	USERNAME_FIELD = 'email'

	class Meta:
		db_table = 'UPWORKS_USER'
		managed = True
		verbose_name = "Usuario"
		verbose_name_plural = "Users"

	def clean(self):
		super().clean()
		self.email = self.__class__.objects.normalize_email(self.email)

	def __str__(self):
		return self.email


