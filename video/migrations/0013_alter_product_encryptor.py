# Generated by Django 4.1.4 on 2022-12-31 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0012_alter_product_encryptor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='encryptor',
            field=models.CharField(blank=True, max_length=1000, null=True, unique=True),
        ),
    ]