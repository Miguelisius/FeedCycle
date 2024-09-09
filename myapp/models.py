from django.db import models

#Cambiar base de datos por tutor con email y psswd y alumnos con nombre y grupo al que pertenecen
#Cada vez que cambio el models, hay que hacer migraciones

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=20)
    url = models.URLField()
    
    def __str__(self):
        return self.title
    
class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

    
#Hacer migraciones por cambio en la base de datos
class Tutor(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=20)
    
    def __str__(self):
        return self.email
class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    pareja = models.CharField(max_length=100)
    grupo = models.CharField(max_length=100)
    
    def __str__(self):
        str(self.nombre) + " " + str(self.grupo)