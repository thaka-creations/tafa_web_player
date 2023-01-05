# Generated by Django 4.1.4 on 2023-01-04 19:24

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppModel',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('serial_number', models.CharField(max_length=1000)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=1000)),
                ('title', models.CharField(blank=True, max_length=1000, null=True)),
                ('short_description', models.CharField(blank=True, max_length=1000, null=True)),
                ('long_description', models.TextField(blank=True, null=True)),
                ('encryptor', models.CharField(blank=True, max_length=1000, null=True, unique=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1000)),
                ('file_extension', models.CharField(blank=True, max_length=255, null=True)),
                ('file_size', models.TextField(blank=True, null=True)),
                ('duration', models.TextField(blank=True, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_videos', to='video.product')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='KeyStorage',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('key', models.CharField(max_length=1000, unique=True)),
                ('time_stamp', models.TextField(blank=True, null=True)),
                ('activated', models.BooleanField(default=False)),
                ('mac_address', models.CharField(blank=True, max_length=1000, null=True)),
                ('watch_time', models.PositiveIntegerField(blank=True, null=True)),
                ('second_screen', models.BooleanField(default=False)),
                ('expires_at', models.DateField(blank=True, null=True)),
                ('validity', models.CharField(blank=True, max_length=1000, null=True)),
                ('watermark', models.TextField(blank=True, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_keys', to='video.product')),
                ('videos', models.ManyToManyField(related_name='video_keys', to='video.video')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
