from django.contrib import admin
from .models import Project, Task, Tutor, Alumno, Grupo, Rubrica, Criterios, NivelDeDesempeno, Descriptores, Notas, Calificacion
# Register your models here.

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Tutor)
admin.site.register(Alumno)
admin.site.register(Grupo)
admin.site.register(Rubrica)
admin.site.register(Criterios)
admin.site.register(NivelDeDesempeno)
admin.site.register(Descriptores)
admin.site.register(Notas)
admin.site.register(Calificacion)