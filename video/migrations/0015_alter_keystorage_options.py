# Generated by Django 4.1.4 on 2022-12-31 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0014_keystorage_time_stamp_keystorage_validity_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='keystorage',
            options={'ordering': ['-created_at']},
        ),
    ]
