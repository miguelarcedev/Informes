# Generated by Django 4.0.6 on 2022-10-09 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('informe', '0002_alter_informe_horas_alter_informe_notas'),
    ]

    operations = [
        migrations.RenameField(
            model_name='informe',
            old_name='estudios_biblicos',
            new_name='estudios',
        ),
    ]
