# Generated by Django 4.1.4 on 2023-01-05 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]