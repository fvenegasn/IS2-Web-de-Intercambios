# Generated by Django 5.0.6 on 2024-06-23 20:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intercambios_caritas', '0048_merge_20240623_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicacion',
            name='categoria_nueva',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='intercambios_caritas.categoria'),
        ),
    ]