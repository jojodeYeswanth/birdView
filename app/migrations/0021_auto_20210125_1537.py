# Generated by Django 3.0.5 on 2021-01-25 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20210125_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='document',
            field=models.ImageField(upload_to='images'),
        ),
        migrations.AlterField(
            model_name='videos',
            name='video_file',
            field=models.FileField(upload_to='videos'),
        ),
    ]
