# Generated by Django 4.1.4 on 2022-12-29 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0003_alter_appmodel_serial_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keystorage',
            name='key',
            field=models.BinaryField(unique=True),
        ),
    ]
