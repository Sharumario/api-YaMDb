# Generated by Django 2.2.16 on 2022-06-20 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220618_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='genres',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
