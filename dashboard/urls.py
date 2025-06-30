from django.urls import path
from .views import CustomLoginView, CustomLogoutView, dashboard_home, project_list, project_detail, task_create, task_edit, add_task_comment, project_create

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', dashboard_home, name='dashboard_home'),
    path('projects/', project_list, name='project_list'),
    path('projects/<int:pk>/', project_detail, name='project_detail'),
    path('projects/<int:project_pk>/tasks/create/', task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', task_edit, name='task_edit'),
    path('tasks/<int:task_pk>/comment/', add_task_comment, name='add_task_comment'),
    path('projects/create/', project_create, name='project_create'),
] 