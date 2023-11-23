# Generated by Django 4.1.3 on 2023-11-12 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('informe', '0008_alter_informe_auxiliar_alter_informe_participacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informe',
            name='auxiliar',
            field=models.CharField(choices=[('Si', 'Si'), (' ', ' ')], default='  ', max_length=10),
        ),
        migrations.AlterField(
            model_name='informe',
            name='notas',
            field=models.CharField(blank=True, choices=[('Inactivo', 'Inactivo'), ('Mudado', 'Mudado'), ('Construccion', 'Construccion'), ('Enfermo', 'Enfermo'), ('Expulsado', 'Expulsado'), ('Reactivado', 'Reactivado'), ('Asamblea', 'Asamblea'), ('Escuela Precursor', 'Escuela Precursor'), ('Inicia Regular', 'Inicia Regular'), ('Nuevo Publicador', 'Nuevo Publicador'), ('Bautismo', 'Bautismo'), ('Readmitido', 'Readmitido')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='informe',
            name='participacion',
            field=models.CharField(choices=[('Si', 'Si'), (' ', ' ')], default='Si', max_length=10),
        ),
        migrations.AlterField(
            model_name='informe',
            name='servicio',
            field=models.CharField(choices=[('Auxiliar', 'Auxiliar'), ('Publicador', 'Publicador'), ('Regular', 'Regular'), ('Especial', 'Especial'), ('Misionero', 'Misionero')], default='Publicador', max_length=10),
        ),
    ]