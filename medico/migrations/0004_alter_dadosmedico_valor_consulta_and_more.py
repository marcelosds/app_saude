# Generated by Django 5.0.4 on 2024-05-03 16:03

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medico', '0003_datasabertas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dadosmedico',
            name='valor_consulta',
            field=models.FloatField(default=100),
        ),
        migrations.AlterField(
            model_name='datasabertas',
            name='data',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]