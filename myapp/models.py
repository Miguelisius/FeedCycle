from django.db import models
#Cada vez que cambio el models, hay que hacer migraciones
class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    pareja = models.CharField(max_length=100)
    grupo = models.CharField(max_length=100)
    
    def __str__(self):
        str(self.nombre) + " " + str(self.grupo)
        
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    alumnos = models.ManyToManyField(Alumno, blank=True)
    
    def __str__(self):
        return self.title
    
    
class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    #alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, null=True, blank=True)
    alumno = models.ManyToManyField(Alumno, blank=True)
    #task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    task = models.ManyToManyField(Task, blank=True)
    
    def __str__(self):
        return self.title
    
class Tutor(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=20)
    project = models.ManyToManyField(Project, blank=True)
    
    def __str__(self):
        return self.email
    
