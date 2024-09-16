from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('about/', views.about),
    path('inicio/', views.home, name='home'),
    path('hello/<str:username>', views.hello),
    path('task/<int>:id', views.tasks),
    path('project/', views.projects),
    path('project_detail/<int:project_id>', views.project_detail, name='project_detail'),
]
