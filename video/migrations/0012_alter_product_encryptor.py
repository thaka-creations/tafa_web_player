# Generated by Django 4.1.4 on 2022-12-31 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0011_product_encryptor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='encryptor',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
