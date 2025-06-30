from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .models import Project, Task, TaskComment
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'dashboard/login.html'

class CustomLogoutView(LogoutView):
    next_page = '/login/'

@login_required
def dashboard_home(request):
    return render(request, 'dashboard/dashboard_home.html')

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assignee', 'status', 'due_date', 'priority']

class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['comment']

@login_required
def project_list(request):
    if request.user.role == 'admin':
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(tasks__assignee=request.user).distinct()
    return render(request, 'dashboard/project_list.html', {'projects': projects})

@login_required
def project_detail(request, pk):
    project = Project.objects.get(pk=pk)
    tasks = project.tasks.all()
    return render(request, 'dashboard/project_detail.html', {'project': project, 'tasks': tasks})

@login_required
def task_create(request, project_pk):
    project = Project.objects.get(pk=project_pk)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return HttpResponseRedirect(reverse('project_detail', args=[project.pk]))
    else:
        form = TaskForm()
    return render(request, 'dashboard/task_form.html', {'form': form, 'project': project})

@login_required
def task_edit(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project_detail', args=[task.project.pk]))
    else:
        form = TaskForm(instance=task)
    return render(request, 'dashboard/task_form.html', {'form': form, 'project': task.project, 'edit': True})

@login_required
def add_task_comment(request, task_pk):
    task = Task.objects.get(pk=task_pk)
    if request.method == 'POST':
        form = TaskCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(reverse('project_detail', args=[task.project.pk]))
    else:
        form = TaskCommentForm()
    return render(request, 'dashboard/task_comment_form.html', {'form': form, 'task': task})
