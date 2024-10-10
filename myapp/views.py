from django.http import HttpResponse, JsonResponse
from .models import Project, Task, Tutor, Alumno, Grupo
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

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
            messages.success(request, 'Proyecto creado exitosamente')

        elif 'create_group' in request.POST:
            project_id = request.POST.get('project_id')
            numero_grupo = request.POST.get('numero_grupo')

            if not project_id or not numero_grupo:
                messages.error(request, 'Debe seleccionar un proyecto y proporcionar un número de grupo.')
                return redirect('home')
            project = get_object_or_404(Project, id_project=project_id, profesor=tutor_mail)
            new_group = Grupo(numero_grupo=numero_grupo, profesor=tutor_mail, project=project)
            new_group.save()

            messages.success(request, f'Grupo {numero_grupo} creado y asignado al proyecto {project.title}')
    
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

def project_detail(request, project_id):
    project = get_object_or_404(Project, id_project=project_id)
    if request.method == 'POST':
        numero_grupo = request.POST.get('numero_grupo')
        
        new_group = Grupo(numero_grupo=numero_grupo, profesor=request.user.tutor)
        new_group.save()
        
        project.grupo = new_group
        project.save()
        messages.success(request, 'Grupo creada exitosamente')
    #grupos = Grupo.objects.filter(profesor=request.user.tutor)
    grupo_asignado = project.grupo
    return render(request, 'registration/project_detail.html', {'project': project, 'grupos': grupo_asignado})

def index(request):
    return render(request,'index.html')

def projects(request):
    project = list(Project.objects.values())
    return JsonResponse(projects, safe=False)

def tasks(request,id):
    task = get_object_or_404(Task, id=id)
    return HttpResponse('task: %s' %task.name)