# Generated by Django 5.0.4 on 2024-06-06 19:43

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intercambios_caritas', '0023_rename_centro_encuentro_intercambio_punto_encuentro_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicacion',
            name='dias_convenientes',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Lunes', 'Lunes'), ('Martes', 'Martes'), ('Miércoles', 'Miércoles'), ('Jueves', 'Jueves'), ('Viernes', 'Viernes'), ('Sábado', 'Sábado'), ('Domingo', 'Domingo')], max_length=100),
        ),
    ]