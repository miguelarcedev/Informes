# Generated by Django 4.0.6 on 2022-10-09 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('totales', '0003_alter_auxiliares_options_alter_publicadores_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auxiliares',
            old_name='estudios_biblicos',
            new_name='estudios',
        ),
        migrations.RenameField(
            model_name='publicadores',
            old_name='estudios_biblicos',
            new_name='estudios',
        ),
        migrations.RenameField(
            model_name='regulares',
            old_name='estudios_biblicos',
            new_name='estudios',
        ),
    ]