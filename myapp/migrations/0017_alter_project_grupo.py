# Generated by Django 5.0.6 on 2024-10-10 16:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_project_grupo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='grupo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.grupo'),
        ),
    ]
