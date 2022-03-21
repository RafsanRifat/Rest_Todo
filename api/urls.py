from django.urls import path, include
from .views import apiOverview, taskList, taskDetail, taskCreate

urlpatterns = [
    path('', apiOverview),
    path('task-list/', taskList, name='task-list'),
    path('task-detail/<str:pk>/', taskDetail, name='task-detail'),
    path('task-create/', taskCreate, name='task-create'),
]
