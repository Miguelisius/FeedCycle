from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('about/', views.about),
    path('inicio/', views.home, name='home'),
    path('hello/<str:username>', views.hello),
    path('task/<int>:id', views.tasks),
    path('project/', views.projects),
]
