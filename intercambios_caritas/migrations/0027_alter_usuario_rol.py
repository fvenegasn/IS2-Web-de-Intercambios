# Generated by Django 4.2.13 on 2024-06-07 11:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("intercambios_caritas", "0026_usuario_rol"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usuario",
            name="rol",
            field=models.CharField(
                choices=[
                    ("Administrador", "Administrador"),
                    ("Usuario", "Usuario"),
                    ("Moderador", "Moderador"),
                ],
                default="Usuario",
                max_length=20,
            ),
        ),
    ]