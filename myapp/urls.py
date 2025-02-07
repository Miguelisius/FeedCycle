from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
#from .views import delete_project, delete_group

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('inicio/', views.home, name='home'),
    path('project_detail/<int:project_id>/group/<int:group_id>/', views.project_detail, name='project_detail'),
    path('task_detail/<int:task_id>', views.task_detail, name='task_detail'),
    path('taskrubric_detail/<int:task_id>', views.taskrubric_detail, name='taskrubric_detail'),
    path('rubric_detail/<int:rubric_id>', views.taskrubric_display, name='rubric_detail'),
    path('correcion/<int:task_id>', views.correccion_rubrica, name='correcion'),
    path('correccion/<int:id_alumno>/<int:id_task>/', views.correccion_personal, name='correccion_personal'),
    path('correccion/<int:id_alumno>/exportar-pdf/<int:id_task>/', views.export_correccion_pdf, name='export_correction_pdf'),
    path('rubrica/<int:rubric_id>/exportar-pdf/', views.export_rubrica_pdf, name='export_rubrica_pdf'),
    path('export_feedback/<int:id_grupo>/<int:id_task>/', views.export_feedback_txt, name='export_feedback'),
    path('obtener-feedbacks/<int:id_grupo>/<int:id_criterio>/<int:id_nivel>/', views.obtener_feedbacks, name='obtener_feedbacks'),
    #path('delete_project/<int:project_id>/', delete_project, name='delete_project'),
    #path('delete_group/<int:group_id>/', delete_group, name='delete_group'),
    #path('delete-alumno/<int:alumno_id>/', views.delete_alumno, name='delete_alumno'),
]
