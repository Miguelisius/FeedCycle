# Generated by Django 5.0.6 on 2025-01-03 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0033_calificacion_explicacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calificacion',
            name='explicacion',
        ),
    ]
