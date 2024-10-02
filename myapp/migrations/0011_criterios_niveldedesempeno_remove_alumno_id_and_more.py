# Generated by Django 5.0.6 on 2024-10-02 10:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_remove_project_technology_remove_project_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Criterios',
            fields=[
                ('id_criterio', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion_criterio', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='NivelDeDesempeno',
            fields=[
                ('id_nivel_desempeno', models.AutoField(primary_key=True, serialize=False)),
                ('nivel', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='alumno',
            name='id',
        ),
        migrations.RemoveField(
            model_name='project',
            name='alumno',
        ),
        migrations.RemoveField(
            model_name='project',
            name='id',
        ),
        migrations.RemoveField(
            model_name='project',
            name='task',
        ),
        migrations.RemoveField(
            model_name='task',
            name='alumnos',
        ),
        migrations.RemoveField(
            model_name='task',
            name='completed',
        ),
        migrations.RemoveField(
            model_name='task',
            name='id',
        ),
        migrations.RemoveField(
            model_name='tutor',
            name='id',
        ),
        migrations.RemoveField(
            model_name='tutor',
            name='project',
        ),
        migrations.AddField(
            model_name='alumno',
            name='id_alumno',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='id_project',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='asignatura',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.project'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='id_task',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tutor',
            name='id_tutor',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='alumno',
            name='pareja',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Descriptores',
            fields=[
                ('id_descriptores', models.AutoField(primary_key=True, serialize=False)),
                ('descripcion', models.TextField()),
                ('criterio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.criterios')),
            ],
        ),
        migrations.CreateModel(
            name='Calificacion',
            fields=[
                ('id_calificacion', models.AutoField(primary_key=True, serialize=False)),
                ('calificacion', models.IntegerField()),
                ('feedback', models.TextField()),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.alumno')),
                ('descriptor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.descriptores')),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id_grupo', models.AutoField(primary_key=True, serialize=False)),
                ('numero_grupo', models.IntegerField()),
                ('profesor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.tutor')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='grupo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.grupo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='grupo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.grupo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='alumno',
            name='grupo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.grupo'),
        ),
        migrations.CreateModel(
            name='Notas',
            fields=[
                ('id_notas', models.AutoField(primary_key=True, serialize=False)),
                ('nota', models.IntegerField()),
                ('descriptor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.descriptores')),
                ('nivel_desempeno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.niveldedesempeno')),
            ],
        ),
        migrations.CreateModel(
            name='Rubrica',
            fields=[
                ('id_rubrica', models.AutoField(primary_key=True, serialize=False)),
                ('tarea', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='myapp.task')),
            ],
        ),
        migrations.AddField(
            model_name='niveldedesempeno',
            name='rubrica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.rubrica'),
        ),
        migrations.AddField(
            model_name='criterios',
            name='rubrica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.rubrica'),
        ),
    ]
