from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_superuser(apps, schema_editor):
    apps.get_model(settings.AUTH_USER_MODEL)(
        username='admin',
        password=make_password('admin'),
        is_staff=True,
        is_superuser=True,
    ).save(using=schema_editor.connection.alias)


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '__latest__'),
    ]
    operations = [
        migrations.RunPython(create_superuser, atomic=True),
    ]
