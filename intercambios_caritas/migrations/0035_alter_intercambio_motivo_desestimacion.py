# Generated by Django 5.0.4 on 2024-06-11 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intercambios_caritas', '0034_alter_intercambio_motivo_desestimacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intercambio',
            name='motivo_desestimacion',
            field=models.CharField(default='N/A', max_length=280),
        ),
    ]