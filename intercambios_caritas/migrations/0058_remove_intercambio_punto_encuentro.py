# Generated by Django 5.0.4 on 2024-07-01 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intercambios_caritas', '0057_intercambio_categoria_nueva_intercambio_filial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intercambio',
            name='punto_encuentro',
        ),
    ]