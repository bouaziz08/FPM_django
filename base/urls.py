from django.urls import path
from .views import TaskList, TaskDetails, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, RegisterPage, TaskConfirm
from . import views
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout_user/', views.logout_user, name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('task/<int:pk>/task-confirm', TaskConfirm.as_view(), name='task-confirm'),

    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetails.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),

    path('Sendemail/', views.sendemail, name='Sendemail'),


]
