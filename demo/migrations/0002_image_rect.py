# Generated by Django 3.0.6 on 2020-05-30 10:52

import demo.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('demo', '0001_create_superuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to=demo.models.uuid_name)),
                ('scanned', models.BooleanField(default=False)),
                ('corrected', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Rect',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.TextField()),
                ('description', models.TextField()),
                ('top', models.IntegerField()),
                ('left', models.IntegerField()),
                ('right', models.IntegerField()),
                ('bottom', models.IntegerField()),
                ('level', models.IntegerField()),
                ('level_corrected', models.IntegerField(blank=True, null=True)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='demo.Image')),
            ],
        ),
    ]
