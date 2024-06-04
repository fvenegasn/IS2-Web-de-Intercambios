# Generated by Django 5.0.6 on 2024-06-04 15:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intercambios_caritas', '0017_intercambio'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicacion',
            name='franja_horaria_fin',
            field=models.TimeField(default=datetime.time(18, 0)),
        ),
        migrations.AddField(
            model_name='publicacion',
            name='franja_horaria_inicio',
            field=models.TimeField(default=datetime.time(9, 0)),
        ),
    ]
