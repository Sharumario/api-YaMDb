# Generated by Django 2.2.16 on 2022-06-17 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(max_length=8, verbose_name='Код подтверждения'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], default='user', max_length=16, verbose_name='Пользовательская роль'),
        ),
    ]
