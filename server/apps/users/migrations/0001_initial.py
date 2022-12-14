# Generated by Django 4.1.1 on 2022-09-22 02:44

import apps.users.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models

from ..insert import insert_init_data, undo_insert_data

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(error_messages={'unique': 'Ya existe un usuario con esete email.'}, help_text='Obligatorio. Correo electronico.', max_length=254, unique=True, verbose_name='Email')),
                ('is_staff', models.BooleanField(default=False, help_text='Designa si el usuario puede iniciar sesión en este sitio de administración', verbose_name='Es staff')),
                ('is_active', models.BooleanField(default=True, help_text='Designa si este usuario debe ser tratado como activo.Desmarcar esto en lugar de eliminar cuentas', verbose_name='Es activo')),
                ('joined_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Ultima modificacion')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Users',
                'db_table': 'UPWORKS_USER',
                'managed': True,
            },
            managers=[
                ('objects', apps.users.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, verbose_name='Nombre')),
                ('description', models.CharField(max_length=30, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Rol',
                'verbose_name_plural': 'Roles',
                'db_table': 'UPWORKS_ROLES_CAT',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='HistoricalUser',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(db_index=True, error_messages={'unique': 'Ya existe un usuario con esete email.'}, help_text='Obligatorio. Correo electronico.', max_length=254, verbose_name='Email')),
                ('is_staff', models.BooleanField(default=False, help_text='Designa si el usuario puede iniciar sesión en este sitio de administración', verbose_name='Es staff')),
                ('is_active', models.BooleanField(default=True, help_text='Designa si este usuario debe ser tratado como activo.Desmarcar esto en lugar de eliminar cuentas', verbose_name='Es activo')),
                ('joined_at', models.DateTimeField(blank=True, editable=False, verbose_name='Fecha de registro')),
                ('update_at', models.DateTimeField(blank=True, editable=False, verbose_name='Ultima modificacion')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Usuario',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(blank=True, help_text='Designa el rol que tendra el usuario', to='users.role', verbose_name='Rol'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.RunPython(insert_init_data, reverse_code=undo_insert_data)
    ]
