# Generated by Django 4.1.1 on 2022-10-25 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicador', '0003_alter_publicador_estado_alter_publicador_grupo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicador',
            name='estado',
            field=models.CharField(choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo'), ('Baja', 'Baja'), ('Mudado', 'Mudado')], max_length=10),
        ),
    ]
