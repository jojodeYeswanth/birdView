# Generated by Django 3.0.5 on 2021-01-24 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_images_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='document',
            field=models.ImageField(upload_to='bird/'),
        ),
    ]
