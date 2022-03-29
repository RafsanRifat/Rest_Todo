from django.urls import path, include
from .views import apiOverview, taskList, taskDetail, taskCreate, taskUpdate, taskDelete, UserRegistrationView, \
    UserLoginView, UserProfileView, UserChangePasswordView, SendPasswordResetEmailView

urlpatterns = [
    path('', apiOverview),
    path('task-list/', taskList, name='task-list'),
    path('task-detail/<str:pk>/', taskDetail, name='task-detail'),
    path('task-create/', taskCreate, name='task-create'),
    path('task-update/<str:pk>/', taskUpdate, name='task-update'),
    path('task-delete/<str:pk>/', taskDelete, name='task-delete'),

    path('registration/', UserRegistrationView.as_view(), name='registrations'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profileview/', UserProfileView.as_view(), name='profileview'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('resetpassword/', SendPasswordResetEmailView.as_view(), name='resetpassword'),

]
