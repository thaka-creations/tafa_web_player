# Generated by Django 4.1.4 on 2022-12-27 10:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('serial_number', models.CharField(max_length=1000, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
