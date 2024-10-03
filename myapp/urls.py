from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('inicio/', views.home, name='home'),
    path('project/', views.projects, name='projects'),
    path('project_detail/<int:project_id>', views.project_detail, name='project_detail'),
]
