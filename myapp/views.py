from django.http import HttpResponse, JsonResponse
from .models import Project, Task, Tutor, Alumno, Grupo, Rubrica, Criterios, NivelDeDesempeno, Descriptores, Notas, Calificacion
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
import csv
from django.urls import reverse
from io import StringIO

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
            archivo_csv = request.FILES['archivo'].read().decode('utf-8').replace('\"', '')
            archivo_io = StringIO(archivo_csv)
            
            reader = csv.reader(archivo_io, delimiter=',' , quotechar='"')
            next(reader)
            print("Leggo aquiantes de row in reader\n")
            for row in reader:
                row = [cell.strip() for cell in row]
                print(len(row))
                #print(row[1])
                #if len(row)<4:
                print("Dentrop del if\n")
                nombre_alumno = row[0].strip()
                apellido = row[1].strip()
                correo=  row[2].strip()
                pareja = None
                #print(nombre_alumno, apellido, correo)
                if Alumno.objects.filter(email=correo).exists():
                    messages.error(request, f'El correo {correo} ya está registrado.')
                    continue
                if len(row) == 4:
                    pareja_str = row[3].strip()
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
            if nombre_alumno and pareja and not Alumno.objects.filter(email=correo).exists():
                Alumno.objects.create(nombre=nombre_alumno, apellido = apellido, email = correo , pareja=pareja, grupo=grupo_asignado)
                messages.success(request, f'Alumno: {nombre_alumno} agregado exitosamente a la pareja: {pareja}.')
                
        if 'create_task' in request.POST:
            task_name = request.POST.get('title')
            task_description = request.POST.get('description')
            
            new_task = Task.objects.create(title=task_name, description=task_description, grupo=grupo_asignado, asignatura=project)
            messages.success(request, 'Tarea creada exitosamente.')
            return redirect('task_detail.html', task_id=new_task.id_task)
    
    alumnos = Alumno.objects.filter(grupo=grupo_asignado)
    tareas = Task.objects.filter(grupo=grupo_asignado)
    return render(request, 'registration/project_detail.html', {
        'project': project,
        'grupo': grupo_asignado,
        'alumnos': alumnos,
        'tareas': tareas,
    })

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id_task=task_id)
    
    return render(request, 'registration/task_detail.html', {
        'task': task,
    }
    )
    
@login_required
def taskrubric_detail(request, task_id):
    task = get_object_or_404(Task, id_task=task_id)
    rubrica, created = Rubrica.objects.get_or_create(tarea=task)
    

    if request.method == 'POST':
        criterio = request.POST.get('criterio')
        nivel = request.POST.get('nivel','').strip()
        descripcion_nivel = request.POST.get('descripcion_nivel',  '').strip()
        if criterio:
            Criterios.objects.create(rubrica=rubrica, descripcion_criterio=criterio)
            messages.success(request, 'Criterio agregado exitosamente.')
        elif nivel or descripcion_nivel:
            #NivelDeDesempeno.objects.create(rubrica=rubrica, nivel=nivel)
            #messages.success(request, 'Nivel de desempeño agregado exitosamente.')
            print("Valor de descripcion_nivel:", descripcion_nivel)
            try:
                new_level = NivelDeDesempeno(
                    rubrica=rubrica,
                    nivel=nivel if nivel else None,
                    descripcion_nivel=descripcion_nivel if descripcion_nivel else None,
                )
                new_level.full_clean()
                new_level.save()
                messages.success(request, 'Nivel de desempeño agregado exitosamente.')
            except ValidationError as e:
                messages.error(request, e)
            nivel_new = NivelDeDesempeno.objects.filter(rubrica=rubrica)
        elif 'save_rubrica' in request.POST:
            criterios = Criterios.objects.filter(rubrica=rubrica)
            niveles = NivelDeDesempeno.objects.filter(rubrica=rubrica)
            
            for c in criterios:
                for n in niveles:
                    descriptor_key = f'descriptor_{c.id_criterio}_{n.id_nivel_desempeno}'
                    descriptor_value = request.POST.get(descriptor_key)
                    if descriptor_value:
                        Descriptores.objects.create(criterio=c, nivel_de_desempeno=n, descripcion= descriptor_value)
            #print("Leggo aqui\n")
            messages.success(request, 'Rúbrica guardada exitosamente.')
            return redirect('rubric_detail', rubric_id= rubrica.id_rubrica)
                    
    #rubricas = Rubrica.objects.filter(tarea=task)
    criterio_new = Criterios.objects.filter(rubrica=rubrica)
    nivel_new = NivelDeDesempeno.objects.filter(rubrica=rubrica)
    print(nivel_new)
    descriptores = []
    for c in criterio_new:
        c_dec = []
        for n in nivel_new:
            descr =  Descriptores.objects.filter(criterio=c, nivel_de_desempeno=n).first()
            c_dec.append(descr.descripcion if descr else '')
        descriptores.append({'criterio': c.descripcion_criterio, 'descriptores':c_dec})
    
    
    return render(request,'registration/taskrubric_detail.html', {
        'task': task,
        'rubricas': [rubrica],
        'criterio' : criterio_new,
        'nivel' : nivel_new,
        'rubrica': rubrica,
        'descriptores': descriptores,
    })
    
@login_required
def taskrubric_display(request, rubric_id):
    #task = get_object_or_404(Task, id_task=task_id)
    rubrica = get_object_or_404(Rubrica, id_rubrica=rubric_id)
    task = rubrica.tarea

    criterios = Criterios.objects.filter(rubrica=rubrica)
    niveles = NivelDeDesempeno.objects.filter(rubrica=rubrica)

    descriptores_list = []
    for criterio in criterios:
        crit_desc = []
        for nivel in niveles:
            descriptor = Descriptores.objects.filter(criterio=criterio, nivel_de_desempeno=nivel).first()
            crit_desc.append(descriptor.descripcion if descriptor else '')
        descriptores_list.append({
            'criterio': criterio.descripcion_criterio,
            'descriptores': crit_desc,
        })

    return render(request, 'registration/rubrica_final.html', {
        'task': task,
        'rubrica': rubrica,
        'criterios': criterios,
        'niveles': niveles,
        'descriptores_list': descriptores_list,
    })
    
@login_required
def correccion_rubrica(request, task_id):
    task = get_object_or_404(Task, id_task=task_id)
    rubrica = Rubrica.objects.filter(tarea=task).first()
    criterios = Criterios.objects.filter(rubrica=rubrica)
    niveles = NivelDeDesempeno.objects.filter(rubrica=rubrica)
    
    alumnos = Alumno.objects.filter(grupo=task.grupo)
    
    descriptores = []
    for c in criterios:
        c_dec = []
        for n in niveles:
            descr = Descriptores.objects.filter(criterio=c, nivel_de_desempeno=n).first()
            c_dec.append(descr.descripcion if descr else '')
        descriptores.append({'criterio': c.descripcion_criterio, 'descriptores': c_dec})
    
    if request.method == 'POST':
        for c in criterios:
            for n in niveles:
                descriptor_key = f'descriptor_{c.id_criterio}_{n.id_nivel_desempeno}'
                descriptor_value = request.POST.get(descriptor_key)
                if descriptor_value:
                    Descriptores.objects.create(criterio=c, nivel_de_desempeno=n, descripcion=descriptor_value)
        messages.success(request, 'Corrección guardada exitosamente.')
        return redirect('rubric_detail', rubric_id=rubrica.id_rubrica)
    
    return render(request, 'registration/correccion.html', {
        'task': task,
        'rubrica': rubrica,
        'criterios': criterios,
        'niveles': niveles,
        'descriptores': descriptores,
        'alumnos': alumnos,
    })
    
@login_required
def correccion_personal(request, id_alumno):
    alumno = get_object_or_404(Alumno, id_alumno=id_alumno)
    pareja = Alumno.objects.filter(grupo = alumno.grupo,pareja=alumno.pareja).exclude()
    
    task = Task.objects.filter(grupo=alumno.grupo).first()
    rubrica = Rubrica.objects.filter(tarea=task).first()
    niveles = NivelDeDesempeno.objects.filter(rubrica=rubrica)
    criterios = Criterios.objects.filter(rubrica=rubrica)
    
    descriptores = []
    for c in criterios:
        c_dec = []
        for n in niveles:
            descr = Descriptores.objects.filter(criterio=c, nivel_de_desempeno=n).first()
            c_dec.append(descr.descripcion if descr else '')
        descriptores.append({'criterio': c.descripcion_criterio, 'descriptores': c_dec})
    
    return render(request, 'registration/correccion_personal.html', {
        'alumno': alumno,
        'pareja': pareja,
        'task': task,
        'rubrica': rubrica,
        'niveles': niveles,
        'descriptores': descriptores,
        'criterios': criterios,
    })


def index(request):
    return render(request,'index.html')

def projects(request):
    project = list(Project.objects.values())
    return JsonResponse(projects, safe=False)

def tasks(request,id):
    task = get_object_or_404(Task, id=id)
    return HttpResponse('task: %s' %task.name)