from django.http import HttpResponse, JsonResponse
from .models import Project, Task, Tutor, Alumno, Grupo
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
import csv

# Create your views here.

def hello(request, username):
    print(username)
    return HttpResponse("<h1>Hello %s. You're at the polls index.</h1>" %username)

def about(request):
    return HttpResponse("<h1>About page</h1>")

@login_required
def home(request):
    try:
        tutor_mail = Tutor.objects.get(user=request.user)
    except Tutor.DoesNotExist:
        messages.error(request, "No se encontró un tutor asociado a este usuario.")
        return redirect('register')
    
    if request.method == 'POST':
        if 'create_project' in request.POST:
            project_name = request.POST.get('project_name')
            description = request.POST.get('description')

            new_project = Project(title=project_name, description=description, profesor=tutor_mail)
            new_project.save()
            messages.success(request, 'Asignatura creada exitosamente')

        elif 'create_group' in request.POST:
            project_id = request.POST.get('project_id')
            numero_grupo = request.POST.get('numero_grupo')

            if not project_id or not numero_grupo:
                messages.error(request, 'Debe seleccionar una asignatura y proporcionar un número de grupo.')
                return redirect('home')
            project = get_object_or_404(Project, id_project=project_id, profesor=tutor_mail)
            new_group = Grupo(numero_grupo=numero_grupo, profesor=tutor_mail, project=project)
            new_group.save()

            messages.success(request, f'Grupo {numero_grupo} creado y asignado a la asignatura {project.title}')
    
    projects = Project.objects.filter(profesor=tutor_mail)
    grupos = Grupo.objects.filter(profesor=tutor_mail)
    return render(request, 'registration/home.html', {'projects': projects, 'grupos': grupos})



def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('registration/register.html')
        
        if Tutor.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado')
            return redirect('registration/register.html')
        user = User.objects.create_user(username=email, password=password)
        tutor = Tutor(user=user,email=email, password=password)
        tutor.save()
        return redirect('login')
    return render(request, 'registration/register.html')




@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id_project=project_id)
    grupo_asignado = Grupo.objects.filter(project=project).first()
    
    if request.method == 'POST':
        if 'archivo' in request.FILES:
            archivo_csv = request.FILES['archivo'].read().decode('utf-8').splitlines()
            reader = csv.reader(archivo_csv, delimiter=',')
            next(reader)
            for row in reader:
                row = [cell.strip() for cell in row]
                if len(row)>=4:
                    nombre_alumno, apellido,correo= row[0], row[1], row[2]
                    pareja = None
                    if len(row) == 4:
                        pareja_str = row[3].strip().replace(';', '')
                        if pareja_str:
                            pareja = int(pareja_str)
                        else:
                            pareja = None
                    Alumno.objects.create(nombre=nombre_alumno, apellido=apellido, email=correo ,pareja=pareja, grupo=grupo_asignado)
            messages.success(request, 'Alumnos agregados desde el archivo CSV exitosamente.')
        
        if 'create_alumno' in request.POST:
            nombre_alumno = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            correo = request.POST.get('email')
            pareja = request.POST.get('pareja')
            if nombre_alumno and pareja:
                Alumno.objects.create(nombre=nombre_alumno, apellido = apellido, email = correo , pareja=pareja, grupo=grupo_asignado)
                messages.success(request, f'Alumno: {nombre_alumno} agregado exitosamente a la pareja: {pareja}.')
                
        if 'create_task' in request.POST:
            task_name = request.POST.get('title')
            task_description = request.POST.get('description')
            
            Task.objects.create(title=task_name, description=task_description, grupo=grupo_asignado, asignatura=project)
            messages.success(request, 'Tarea creada exitosamente.')
    
    alumnos = Alumno.objects.filter(grupo=grupo_asignado)
    tareas = Task.objects.filter(grupo=grupo_asignado)
    return render(request, 'registration/project_detail.html', {
        'project': project,
        'grupo': grupo_asignado,
        'alumnos': alumnos,
        'tareas': tareas,
    })


def index(request):
    return render(request,'index.html')

def projects(request):
    project = list(Project.objects.values())
    return JsonResponse(projects, safe=False)

def tasks(request,id):
    task = get_object_or_404(Task, id=id)
    return HttpResponse('task: %s' %task.name)