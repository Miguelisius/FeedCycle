# Generated by Django 5.0.6 on 2024-11-07 16:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0029_remove_notas_pareja_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='notas',
            name='alumno',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='correcciones', to='myapp.alumno'),
        ),
    ]
