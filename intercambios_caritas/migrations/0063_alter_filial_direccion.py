# Generated by Django 5.0.6 on 2024-07-03 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intercambios_caritas', '0062_filial_direccion_alter_filial_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filial',
            name='direccion',
            field=models.CharField(default='A confirmar', max_length=100, verbose_name='Dirección'),
        ),
    ]