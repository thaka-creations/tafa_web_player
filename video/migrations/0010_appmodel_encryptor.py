# Generated by Django 4.1.4 on 2023-01-19 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0009_appmodel_model_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='appmodel',
            name='encryptor',
            field=models.BooleanField(default=False),
        ),
    ]
