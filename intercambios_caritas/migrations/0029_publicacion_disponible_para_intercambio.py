# Generated by Django 5.0.4 on 2024-06-07 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intercambios_caritas', '0028_remove_intercambio_aceptada_intercambio_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicacion',
            name='disponible_para_intercambio',
            field=models.BooleanField(default=True),
        ),
    ]