# Generated by Django 4.1.4 on 2023-01-02 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0017_alter_video_options_alter_video_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='long_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='short_description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='title',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]