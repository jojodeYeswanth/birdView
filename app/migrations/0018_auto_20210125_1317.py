# Generated by Django 3.0.5 on 2021-01-25 07:47

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20210125_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='document',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location='/media/photos'), upload_to=''),
        ),
    ]
