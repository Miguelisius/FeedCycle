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
    #username = request.user.username
    #return HttpResponse("<h1>HOLA %s. Bienvenido a la página principal</h1>" %username)
    tutor_mail, created = Tutor.objects.get_or_create(email=request.user.email)
    
    if request.method == 'POST':
        #creacipn de la asignatura (cosas que editar url y technology )
        project_name = request.POST.get('project_name')
        description = request.POST.get('description')
        
        new_project = Project(title = project_name,description=description)
        new_project.save()
        
        tutor_mail.project.add(new_project)
        tutor_mail.save()
        messages.success(request, 'Proyecto creado exitosamente')
        
    projects = Project.objects.all()
    return render(request, 'registration/home.html', {'projects': projects})
        
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
    grupos = Grupo.objects.filter(profesor=request.user.tutor)
    return render(request, 'registration/project_detail.html', {'project': project, 'grupos': grupos})

def index(request):
    return render(request,'index.html')

def projects(request):
    project = list(Project.objects.values())
    return JsonResponse(projects, safe=False)

def tasks(request,id):
    task = get_object_or_404(Task, id=id)
    return HttpResponse('task: %s' %task.name)