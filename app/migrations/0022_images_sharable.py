# Generated by Django 3.0.5 on 2021-01-25 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20210125_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='sharable',
            field=models.IntegerField(default=0),
        ),
    ]
