from django.contrib import admin
from .models import Project, Task, Tutor, Alumno
# Register your models here.

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Tutor)
admin.site.register(Alumno)