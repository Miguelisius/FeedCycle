# Generated by Django 5.0.6 on 2025-01-03 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0034_remove_calificacion_explicacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calificacion',
            name='calificacion',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
