# Generated by Django 4.1.4 on 2024-01-02 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='congregacion',
            name='on_trial',
        ),
        migrations.RemoveField(
            model_name='congregacion',
            name='paid_until',
        ),
    ]
