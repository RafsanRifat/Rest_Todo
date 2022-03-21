from django.urls import path, include
from .views import apiOverview, taskList

urlpatterns = [
    path('', apiOverview),
    path('task-list/', taskList)
]
