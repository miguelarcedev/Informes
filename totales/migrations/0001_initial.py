# Generated by Django 4.0.6 on 2022-08-11 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Totales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('año', models.IntegerField()),
                ('mes', models.CharField(choices=[('Enero', 'Enero'), ('Febrero', 'Febrero'), ('Marzo', 'Marzo'), ('Abril', 'Abril'), ('Mayo', 'Mayo'), ('Junio', 'Junio'), ('Julio', 'Julio'), ('Agosto', 'Agosto'), ('Septiembre', 'Septiembre'), ('Octubre', 'Octubre'), ('Noviembre', 'Noviembre'), ('Diciembre', 'Diciembre')], max_length=10)),
                ('publicaciones_p', models.IntegerField(blank=True, null=True)),
                ('videos_p', models.IntegerField(blank=True, null=True)),
                ('horas_p', models.IntegerField(blank=True, default=0, null=True)),
                ('revisitas_p', models.IntegerField(blank=True, null=True)),
                ('estudios_biblicos_p', models.IntegerField(blank=True, null=True)),
                ('informan_p', models.IntegerField(blank=True, null=True)),
                ('publicaciones_a', models.IntegerField(blank=True, null=True)),
                ('videos_a', models.IntegerField(blank=True, null=True)),
                ('horas_a', models.IntegerField(blank=True, default=0, null=True)),
                ('revisitas_a', models.IntegerField(blank=True, null=True)),
                ('estudios_biblicos_a', models.IntegerField(blank=True, null=True)),
                ('informan_a', models.IntegerField(blank=True, null=True)),
                ('publicaciones_r', models.IntegerField(blank=True, null=True)),
                ('videos_r', models.IntegerField(blank=True, null=True)),
                ('horas_r', models.IntegerField(blank=True, default=0, null=True)),
                ('revisitas_r', models.IntegerField(blank=True, null=True)),
                ('estudios_biblicos_r', models.IntegerField(blank=True, null=True)),
                ('informan_r', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'total',
                'verbose_name_plural': 'totales',
                'ordering': ['año'],
            },
        ),
    ]
