def insert_init_data(apps, schema_editor):
	Roles = apps.get_model("users", "Role")
	db_alias = schema_editor.connection.alias
	Roles.objects.using(db_alias).bulk_create([
		Roles(id=1, name="EMPLOYEE"),
		Roles(id=2, name="RECLUTER"),
		Roles(id=3, name="ADMIN"),
	])

def undo_insert_data(apps, schema_editor): 
	pass