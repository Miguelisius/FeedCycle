from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('inicio/', views.home, name='home'),
    path('project/', views.projects, name='projects'),
    path('project_detail/<int:project_id>', views.project_detail, name='project_detail'),
    path('task_detail/<int:task_id>', views.task_detail, name='task_detail'),
    path('taskrubric_detail/<int:task_id>', views.taskrubric_detail, name='taskrubric_detail'),
    path('rubric_detail/<int:rubric_id>', views.taskrubric_display, name='rubric_detail'),
    path('correcion/<int:task_id>', views.correccion_rubrica, name='correcion'),
]
