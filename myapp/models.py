from django.db import models
from django.contrib.auth.models import User
#Cada vez que cambio el models, hay que hacer migraciones

class Tutor(models.Model):
    id_tutor = models.AutoField(primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    #project = models.ManyToManyField('Project', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return f"Profesor {self.id_tutor}"


class Project(models.Model): #Asignatura
    id_project = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    profesor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    #grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True, blank=True)
    
    
    def __str__(self):
        return self.title

class Grupo(models.Model):
    id_grupo = models.AutoField(primary_key=True)
    profesor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    numero_grupo = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Grupo {self.numero_grupo}"
class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    pareja = models.IntegerField(null=True, blank=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        str(self.nombre) + " " + str(self.grupo)
        
class Task(models.Model): #Tarea
    id_task = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    #completed = models.BooleanField(default=False)
    #alumnos = models.ManyToManyField(Alumno, blank=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
class Rubrica(models.Model):
    id_rubrica = models.AutoField(primary_key=True)
    tarea = models.OneToOneField(Task, on_delete=models.CASCADE)
    checked = models.BooleanField(default=False) #Boton de checkbox para ver si se calcula la media de la nota

    def __str__(self):
        return f"Rúbrica de {self.tarea.title}"
    

class Criterios(models.Model):
    id_criterio = models.AutoField(primary_key=True)
    rubrica = models.ForeignKey(Rubrica, on_delete=models.CASCADE)
    descripcion_criterio = models.TextField()

    def __str__(self):
        return f"Criterio {self.id_criterio} - {self.descripcion_criterio[:30]}"
    
class NivelDeDesempeno(models.Model):
    id_nivel_desempeno = models.AutoField(primary_key=True)
    rubrica = models.ForeignKey(Rubrica, on_delete=models.CASCADE)
    nivel = models.TextField(blank=True, null=True)
    descripcion_nivel = models.TextField(blank=True, null=True)

    def clean(self):
        if not self.nivel and not self.descripcion_nivel:
            raise ValidationError('Debe ingresar un nivel o descripción de nivel')

    def __str__(self):
        return f"Nivel {self.nivel}"
    
        
    
class Descriptores(models.Model):
    id_descriptores = models.AutoField(primary_key=True)
    criterio = models.ForeignKey(Criterios, on_delete=models.CASCADE)
    descripcion = models.TextField()
    nivel_de_desempeno = models.ForeignKey(NivelDeDesempeno, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion[:30]
    
class Notas(models.Model):
    id_notas = models.AutoField(primary_key=True)
    nivel_desempeno = models.ForeignKey(NivelDeDesempeno, on_delete=models.CASCADE)
    descriptor = models.ForeignKey(Descriptores, on_delete=models.CASCADE)
    criterio = models.ForeignKey(Criterios, on_delete=models.CASCADE)
    nota = models.IntegerField(null=True, blank=True)
    calificacion_descriptivo = models.TextField(blank=True, null=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE,related_name="correcciones", null=True)
    corregida = models.BooleanField(default=False)
    def __str__(self):
        return f"Nota: {self.nota}"


class Calificacion(models.Model):
    id_calificacion = models.AutoField(primary_key=True)
    descriptor = models.ForeignKey(Descriptores, on_delete=models.CASCADE)
    calificacion = models.IntegerField(null=True, blank=True)
    feedback = models.TextField()
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)

    def __str__(self):
        return f"Calificación: {self.calificacion} para {self.alumno.nombre}"
class FeedbackHistory(models.Model):
    id_feedback = models.AutoField(primary_key=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    criterio = models.ForeignKey(Criterios, on_delete=models.CASCADE)
    nivel_de_desempeno = models.ForeignKey(NivelDeDesempeno, on_delete=models.CASCADE)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    def __str__(self):
        return f"Feedback del grupo {self.grupo.numero_grupo} en {self.fecha.strftime('%Y-%m-%d %H:%M:%S')}"
