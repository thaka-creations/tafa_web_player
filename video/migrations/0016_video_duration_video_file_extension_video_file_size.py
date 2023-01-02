# Generated by Django 4.1.4 on 2023-01-02 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0015_alter_keystorage_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='duration',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='file_extension',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='video',
            name='file_size',
            field=models.TextField(blank=True, null=True),
        ),
    ]
