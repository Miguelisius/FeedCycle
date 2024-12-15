import json
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
from weasyprint import HTML
from django.template.loader import render_to_string



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
        try:
            if 'create_project' in request.POST:
                project_name = request.POST.get('project_name')
                description = request.POST.get('description')

                Project.objects.create(title=project_name, description=description, profesor=tutor_mail)
                messages.success(request, 'Asignatura creada exitosamente.')

            elif 'create_group' in request.POST:
                project_id = request.POST.get('project_id')
                numero_grupo = request.POST.get('numero_grupo')

                if not project_id or not numero_grupo:
                    messages.error(request, 'Debe proporcionar un número de grupo y seleccionar una asignatura.')
                else:
                    project = get_object_or_404(Project, id_project=project_id, profesor=tutor_mail)
                    Grupo.objects.create(numero_grupo=numero_grupo, profesor=tutor_mail, project=project)
                    messages.success(request, 'Grupo creado exitosamente.')

            elif 'delete_project' in request.POST:
                project_id = request.POST.get('delete_project')
                with transaction.atomic():
                    project = get_object_or_404(Project, id_project=project_id)
                    project.delete()
                    messages.success(request, 'Asignatura eliminada exitosamente.')

            elif 'delete_group' in request.POST:
                group_id = request.POST.get('delete_group')
                with transaction.atomic():
                    grupo = get_object_or_404(Grupo, id_grupo=group_id)
                    grupo.delete()
                    messages.success(request, 'Grupo eliminado exitosamente.')
            elif 'update_project' in request.POST:
                project_id = request.POST.get('edit_project_id')
                new_project_title = request.POST.get('edit_project_name')
                new_project_description = request.POST.get('edit_description')
                project = get_object_or_404(Project, id_project=project_id)
                project.title = new_project_title
                project.description = new_project_description
                project.save()
                messages.success(request, 'Asignatura actualizada exitosamente.')

            elif 'update_group' in request.POST:
                group_id = request.POST.get('edit_group_id')
                new_group_number = request.POST.get('edit_group_number')
                grupo = Grupo.objects.get(id_grupo=group_id, profesor=tutor_mail)
                grupo.numero_grupo = new_group_number
                grupo.save()
                messages.success(request, f"Grupo actualizado exitosamente a '{new_group_number}'.")

        except Exception as e:
            messages.error(request, f"Ocurrió un error: {str(e)}")
        return redirect('home')

    projects = Project.objects.filter(profesor=tutor_mail).prefetch_related('grupo_set')
    grupos = Grupo.objects.filter(profesor=tutor_mail)

    return render(request, 'registration/home.html', {
        'projects': projects,
        'grupos': grupos,
    })

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
def project_detail(request, project_id, group_id):
    project = get_object_or_404(Project, id_project=project_id)
    grupo_asignado = get_object_or_404(Grupo,project=project,id_grupo=group_id)
    show_toast = False
    toast_message = ""
    if request.method == 'POST':
        if 'csv_file' in request.FILES:
            archivo_csv = request.FILES['csv_file'].read().decode('utf-8').replace('\"', '')
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
            
            show_toast = True
            toast_message = "Archivo importado exitosamente."
            
        if 'delete_alumno' in request.POST:
            print("Entro en delete_alumno")
            alumno_id = request.POST.get('id_alumno')
            alumno = get_object_or_404(Alumno, id_alumno=alumno_id)
            alumno_name = alumno.nombre
            alumno.delete()
            
            show_toast = True
            toast_message = f'Alumno "{alumno_name}" eliminado exitosamente.'
            return redirect('project_detail', project_id=project_id, group_id=group_id)
        
        if 'delete_task' in request.POST:
            task_id = request.POST.get('id_task')
            task = get_object_or_404(Task, id_task=task_id)
            task_name = task.title
            task.delete()
            show_toast = True
            toast_message = f'Tarea "{task_name}" eliminada exitosamente.'
            return redirect('project_detail', project_id=project_id, group_id=group_id)
        
        if 'create_alumno' in request.POST:
            nombre_alumno = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            correo = request.POST.get('email')
            pareja = request.POST.get('pareja')
            grupo = Alumno.objects.filter(grupo_id=grupo_asignado.id_grupo)
            #print("Contiene Correo de grupo: ", grupo.contains(correo))
            #if grupo.contains(correo): 
            print("Grupo: "+ str(grupo_asignado.id_grupo))
            
            if nombre_alumno and pareja and not Alumno.objects.filter(email=correo, grupo=grupo_asignado.id_grupo).exists():
                Alumno.objects.create(nombre=nombre_alumno, apellido = apellido, email = correo , pareja=pareja, grupo=grupo_asignado)
                show_toast = True
                toast_message = f'Alumno {nombre_alumno} agregado exitosamente.'
            else:
                messages.error(request, f'El Alumno {nombre_alumno} {apellido} con correo: {correo} ya está registrado.')
            
        if 'create_task' in request.POST:
            task_name = request.POST.get('title')
            task_description = request.POST.get('description')
            
            new_task = Task.objects.create(title=task_name, description=task_description, grupo=grupo_asignado, asignatura=project)
            show_toast = True
            toast_message = "Tarea creada exitosamente."
            #return redirect('registration/task_detail.html', task_id=new_task.id_task)
        """
        if 'update_alumno' in request.POST:
            alumno_id = request.POST.get('edit_alumno_id')
            new_name = request.POST.get('edit_nombre')
            new_apellido = request.POST.get('edit_apellido')
            new_email = request.POST.get('edit_email')
            new_pareja = request.POST.get('edit_pareja')
            alumno = get_object_or_404(Alumno, id_alumno=alumno_id)
            alumno.nombre = new_name
            alumno.apellido = new_apellido
            alumno.email = new_email
            alumno.pareja = new_pareja
            alumno.save()
            messages.success(request, f'Alumno actualizado exitosamente.')
        
        
        """
    
    alumnos = Alumno.objects.filter(grupo=grupo_asignado)
    tareas = Task.objects.filter(grupo=grupo_asignado)
    return render(request, 'registration/project_detail.html', {
        'project': project,
        'grupo': grupo_asignado,
        'alumnos': alumnos,
        'tareas': tareas,
        'show_toast': show_toast,
        'toast_message': toast_message,
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
    
    show_toast = False
    toast_message = ""
    modal = None
    tabla = False
    #media =False
    if request.method == 'POST':
        criterio = request.POST.get('criterio')
        nivel = request.POST.get('nivel','').strip()
        descripcion_nivel = request.POST.get('descripcion_nivel',  '').strip()
        calcular_media = request.POST.get('calcular_media')
        
        #print("Valor de calcular_media:", calcular_media)
        if criterio:
            Criterios.objects.create(rubrica=rubrica, descripcion_criterio=criterio)
            #messages.success(request, 'Criterio agregado exitosamente.')
            toast_message = "Criterio agregado exitosamente."
            modal = 'criterioModal'
            show_toast = True
            
        elif calcular_media is not None:
            #Obtener ek valor del checkedbox y almacenarlo en la BD (cambia models)
            #media = request.POST.get('calcular_media')=='True'
            #media.save()
            rubrica.checked = calcular_media == 'True'
            rubrica.save()
            #print("Valor de media: ", calcular_media)
            #rubrica.checked = media
            #rubrica.save()
            #messages.success(request, 'Rúbrica guardada exitosamente.')
            modal = 'nivelModal'
        
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
                #messages.success(request, 'Nivel de desempeño agregado exitosamente.')
                toast_message = "Nivel de desempeño agregado exitosamente."
                show_toast = True
                modal = 'nivelModal'
            except ValidationError as e:
                #messages.error(request, e)
                toast_message = f"Error al agregar nivel: {e}"
                show_toast = True
            nivel_new = NivelDeDesempeno.objects.filter(rubrica=rubrica)
        #elif 'fin_modal' in request.POST:
        # tabla = True
        elif 'save_rubrica' in request.POST:# or 'fin_modal' in request.POST:
            #print("Leggo aqui 7777777777\n")
            criterios = Criterios.objects.filter(rubrica=rubrica)
            niveles = NivelDeDesempeno.objects.filter(rubrica=rubrica)
            tabla = True
            for c in criterios:
                for n in niveles:
                    descriptor_key = f'descriptor_{c.id_criterio}_{n.id_nivel_desempeno}'
                    descriptor_value = request.POST.get(descriptor_key)
                    if descriptor_value:
                        Descriptores.objects.create(criterio=c, nivel_de_desempeno=n, descripcion= descriptor_value)
            #print("Leggo aqui\n")
            #if 'save_rubrica' in request.POST:
            #rubrica.checked = calcular_media
            #print("Valor de calcular_media:", calcular_media)
            #rubrica.save()
            #messages.success(request, 'Rúbrica guardada exitosamente.')
            toast_message = "Rúbrica guardada exitosamente."
            show_toast = True
            modal = None
            return redirect('rubric_detail', rubric_id= rubrica.id_rubrica)
            #else:
                #tabla = True
                #modal = None

    #rubricas = Rubrica.objects.filter(tarea=task)
    criterio_new = Criterios.objects.filter(rubrica=rubrica)
    nivel_new = NivelDeDesempeno.objects.filter(rubrica=rubrica)
    #print(nivel_new)
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
        'modal': modal,
        'show_toast': show_toast,
        'toast_message': toast_message,
        #'checked': rubrica.checked,
        #'tabla': tabla,
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
    pareja = Alumno.objects.filter(grupo=alumno.grupo, pareja=alumno.pareja).exclude(id_alumno=alumno.id_alumno).first()
    pareja_alumno = alumno.pareja
    
    
    task = Task.objects.filter(grupo=alumno.grupo).first()
    rubrica = Rubrica.objects.filter(tarea=task).first()
    niveles = NivelDeDesempeno.objects.filter(rubrica=rubrica)
    criterios = Criterios.objects.filter(rubrica=rubrica)
    calificacion = rubrica.checked
    
    descriptores = [
        {
            'criterio': c.descripcion_criterio,
            'descriptores': [
                Descriptores.objects.filter(criterio=c, nivel_de_desempeno=n).first().descripcion
                if Descriptores.objects.filter(criterio=c, nivel_de_desempeno=n).exists()
                else ''
                for n in niveles
            ],
        }
        for c in criterios
    ]
    correccion_guardada = Notas.objects.filter(alumno=alumno, nivel_desempeno__rubrica=rubrica).exists()
    correccion_pareja = pareja and Notas.objects.filter(
        alumno=pareja,
        nivel_desempeno__rubrica=rubrica,
        descriptor__criterio__rubrica=rubrica
    ).exists()
    
    #print("Esto es correccion_guardada: "+str(correccion_guardada))
    """
    if pareja:
        correccion_pareja = Notas.objects.filter(
            alumno=pareja,
            nivel_desempeno__rubrica=rubrica,
            descriptor__criterio__rubrica=rubrica
        ).exists()"""
    
    #print("Mi pareja tiene la correcion: "+str(correccion_pareja))
    #print("Checked: "+str(calificacion))
    calificaciones = []
    if correccion_guardada or correccion_pareja:
        #print(pareja_alumno)
        #print("Me meto en el if")
        alumno_referencia = alumno if correccion_guardada else pareja
        for c in criterios:
            calif_desc = []
            for n in niveles:
                descriptor = Descriptores.objects.filter(criterio=c, nivel_de_desempeno=n).first()
                nota = Notas.objects.filter(nivel_desempeno=n, descriptor=descriptor, alumno=alumno_referencia).first()
                calificacion_num = Calificacion.objects.filter(descriptor=descriptor, alumno=alumno_referencia).first()
                calif_desc.append({
                    'descriptiva': nota.calificacion_descriptivo if nota else '',
                    'numerica': calificacion_num.calificacion if calificacion_num else ''
                })
            calificaciones.append({'criterio': c.descripcion_criterio, 'calificaciones': calif_desc})
        
            print(calificaciones)
    
    if request.method == 'POST' and ((correccion_guardada == False ) or (correccion_pareja == False)):
        #print("Me meto en el POST")
        #print(correccion_guardada)
        #print(correccion_pareja)
        if 'fin_corregir' in request.POST :
            
            crit = Criterios.objects.filter(rubrica=rubrica)
            niv = NivelDeDesempeno.objects.filter(rubrica=rubrica)
            
            for c in crit:
                for n in niv:
                    descriptor_key = f'descriptor_descriptor_{n.descripcion_nivel}_{n.id_nivel_desempeno}'
                    calificacion_key = f'calificacion_{n.descripcion_nivel}_{n.id_nivel_desempeno}'

                    descriptor_value = request.POST.get(descriptor_key)
                    calificacion_value = request.POST.get(calificacion_key)

                    #nota = request.POST.get(descriptor_nota)
                    #print("Esto es descriptor_nota: "+descriptor_nota)
                    #nota_descriptiva = request.POST.get(descriptor_nota)
                    print("ENTROOOOOOOOOOOOOOOOOOOOOOOOOO")
                    #print(nota_descriptiva)
                    #descr, created = Descriptores.objects.get_or_create(criterio=c, nivel_de_desempeno=n)
                    #print(descr)
                    if descriptor_value:
                        descriptor, _ = Descriptores.objects.get_or_create(criterio=c, nivel_de_desempeno=n)
                        Notas.objects.update_or_create(
                            nivel_desempeno=n,
                            descriptor=descriptor,
                            alumno=alumno,
                            defaults={'calificacion_descriptivo': descriptor_value}
                        )
                        if calificacion and calificacion_value:
                            Calificacion.objects.update_or_create(
                                descriptor=descriptor,
                                alumno=alumno,
                                defaults={'calificacion': int(calificacion_value)}
                            )
            correccion_guardada = True
            correccion_pareja = True
            return redirect('correccion_personal', id_alumno=id_alumno)
            #return redirect('correccion_personal', id_alumno=id_alumno)
        
    return render(request, 'registration/correccion_personal.html', {
        'alumno': alumno,
        'pareja': pareja,
        'task': task,
        'rubrica': rubrica,
        'niveles': niveles,
        'descriptores': descriptores,
        'criterios': criterios,
        'calificaciones': calificaciones,
        'correccion_guardada': correccion_guardada,
        'correccion_pareja': correccion_pareja,
        'task_id': task.id_task,
        'calificacion': calificacion,
    })
    """
    for c in criterios:
            calif_desc = []
            for n in niveles:
                nota_descr = Notas.objects.filter(nivel_desempeno=n, descriptor=Descriptores.objects.get(criterio=c, nivel_de_desempeno=n),alumno=alumno).first()
                calif_desc.append(nota_descr.calificacion_descriptivo if nota_descr else '')
            calif.append({'criterio': c.descripcion_criterio, 'calificaciones': calif_desc})
    return render(request, 'registration/correccion_personal.html', {
        'alumno': alumno,
        'pareja': pareja,
        'task': task,
        'rubrica': rubrica,
        'niveles': niveles,
        'descriptores': descriptores,
        'criterios': criterios,
        'calificaciones': calif,
    })"""

@login_required
def export_rubrica_pdf(request, rubric_id):
    rubrica = get_object_or_404(Rubrica, id_rubrica=rubric_id)
    task = rubrica.tarea
    criterios = Criterios.objects.filter(rubrica=rubrica)
    niveles = NivelDeDesempeno.objects.filter(rubrica=rubrica).exclude(nivel__isnull=True, descripcion_nivel__isnull=True)

    descriptores = []
    for c in criterios:
        c_dec = []
        for n in niveles:
            descr = Descriptores.objects.filter(criterio=c, nivel_de_desempeno=n).first()
            if descr and descr.nivel_de_desempeno:
                c_dec.append(descr.descripcion)
            else:
                c_dec.append('Sin descriptor')
        descriptores.append({'criterio': c.descripcion_criterio, 'descriptores': c_dec})
    

    context = {
        'task': task,
        'rubrica': rubrica,
        'criterios': criterios,
        'niveles': niveles,
        'descriptores': descriptores,
    }
    
    html_string = render_to_string('registration/rubrica_finalpdf.html', context)
    pdf = HTML(string=html_string).write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Rubrica_{task.title}.pdf"'
    
    return response


@login_required
def export_correccion_pdf(request, id_alumno):
    alumno = get_object_or_404(Alumno, id_alumno=id_alumno)
    pareja = Alumno.objects.filter(grupo=alumno.grupo, pareja=alumno.pareja).exclude(id_alumno=alumno.id_alumno).first()
    task = Task.objects.filter(grupo=alumno.grupo).first()
    rubrica = Rubrica.objects.filter(tarea=task).first()
    criterios = Criterios.objects.filter(rubrica=rubrica)
    niveles = NivelDeDesempeno.objects.filter(rubrica=rubrica)
    
    calificaciones = []
    for criterio in criterios:
        calif_desc = []
        for nivel in niveles:
            descriptor = Descriptores.objects.filter(criterio=criterio, nivel_de_desempeno=nivel).first()
            nota = Notas.objects.filter(nivel_desempeno=nivel, descriptor=descriptor, alumno=alumno).first()
            calificacion_num = Calificacion.objects.filter(descriptor=descriptor, alumno=alumno).first()

            calif_desc.append({
                'descriptiva': nota.calificacion_descriptivo if nota else 'Sin descripción',
                'numerica': calificacion_num.calificacion if calificacion_num else ''
            })
        calificaciones.append({'criterio': criterio.descripcion_criterio, 'calificaciones': calif_desc})
    
    context = {
        'alumno': alumno,
        'pareja': pareja,
        'task': task,
        'rubrica': rubrica,
        'criterios': criterios,
        'niveles': niveles,
        'calificaciones': calificaciones,
    }
    
    html_string = render_to_string('registration/correccion_personalpdf.html', context)
    pdf = HTML(string=html_string).write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Correccion_{alumno.nombre}_{alumno.apellido}.pdf"'
    
    return response

def index(request):
    return render(request,'index.html')

def projects(request):
    project = list(Project.objects.values())
    return JsonResponse(projects, safe=False)

def tasks(request,id):
    task = get_object_or_404(Task, id=id)
    return HttpResponse('task: %s' %task.name)