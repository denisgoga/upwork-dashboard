from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .models import Project, Task, TaskComment, CustomUser
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from django.db.models import Count
from django.contrib import messages
from django.http import HttpResponseForbidden

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'dashboard/login.html'

class CustomLogoutView(LogoutView):
    next_page = '/login/'

@login_required
def dashboard_home(request):
    from .models import Task, Project
    task_stats = Task.objects.values('status').annotate(count=Count('id'))
    total_projects = Project.objects.count()
    total_tasks = Task.objects.count()
    stats = {s['status']: s['count'] for s in task_stats}
    developers = CustomUser.objects.filter(role='developer')
    return render(request, 'dashboard/dashboard_home.html', {
        'stats': stats,
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'developers': developers,
    })

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
    # Vetëm admin mund të editojë të gjitha fushat, developer vetëm statusin
    if request.user.role == 'admin':
        class AdminTaskForm(TaskForm):
            class Meta(TaskForm.Meta):
                fields = ['title', 'description', 'assignee', 'status', 'due_date', 'priority']
        FormClass = AdminTaskForm
    else:
        # Developer mund të ndryshojë vetëm statusin e detyrave ku është assignee
        if task.assignee != request.user:
            return HttpResponseForbidden()
        class DevTaskForm(forms.ModelForm):
            class Meta:
                model = Task
                fields = ['status']
                widgets = {
                    'status': forms.Select(attrs={'class': 'form-select block w-full rounded border-gray-300 focus:border-blue-500 focus:ring-blue-500'}),
                }
        FormClass = DevTaskForm
    if request.method == 'POST':
        form = FormClass(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project_detail', args=[task.project.pk]))
    else:
        form = FormClass(instance=task)
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

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input block w-full rounded border-gray-300 focus:border-blue-500 focus:ring-blue-500', 'placeholder': 'Project name'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea block w-full rounded border-gray-300 focus:border-blue-500 focus:ring-blue-500', 'rows': 3, 'placeholder': 'Project description'}),
        }

@login_required
def project_create(request):
    if not request.user.role == 'admin':
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project created successfully!')
            return HttpResponseRedirect(reverse('project_list'))
    else:
        form = ProjectForm()
    return render(request, 'dashboard/project_form.html', {'form': form})

@login_required
def project_delete(request, pk):
    if request.user.role != 'admin':
        return HttpResponseForbidden()
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return HttpResponseRedirect(reverse('project_list'))
    return render(request, 'dashboard/project_confirm_delete.html', {'project': project})

@login_required
def task_delete(request, pk):
    if request.user.role != 'admin':
        return HttpResponseForbidden()
    task = get_object_or_404(Task, pk=pk)
    project_pk = task.project.pk
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return HttpResponseRedirect(reverse('project_detail', args=[project_pk]))
    return render(request, 'dashboard/task_confirm_delete.html', {'task': task})
