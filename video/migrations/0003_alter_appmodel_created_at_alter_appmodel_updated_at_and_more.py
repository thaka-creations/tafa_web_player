# Generated by Django 4.1.4 on 2023-01-04 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_alter_appmodel_created_at_alter_appmodel_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='appmodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='keystorage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='keystorage',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]