# Generated by Django 4.0.6 on 2022-10-24 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publicador', '0002_alter_publicador_a_sm_alter_publicador_regular'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicador',
            name='estado',
            field=models.CharField(choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo'), ('Baja', 'Baja'), ('Mudado', 'Mudado'), ('Fallecido', 'Fallecido')], max_length=10),
        ),
        migrations.AlterField(
            model_name='publicador',
            name='grupo',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], max_length=1),
        ),
        migrations.AlterField(
            model_name='publicador',
            name='u_oo',
            field=models.CharField(choices=[('Otras Ovejas', 'Otras Ovejas'), ('Ungido', 'Ungido')], default='Otras Ovejas', max_length=15),
        ),
    ]