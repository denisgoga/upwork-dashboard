from django import forms
from .models import Task, TaskComment

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assignee', 'status', 'due_date', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input block w-full rounded border-gray-300 focus:border-blue-500 focus:ring-blue-500', 'placeholder': 'Enter task title'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea block w-full rounded border-gray-300 focus:border-blue-500 focus:ring-blue-500', 'rows': 4, 'placeholder': 'Enter task description'}),
            'assignee': forms.Select(attrs={'class': 'form-select block w-full rounded border-gray-300 focus:border-blue-500 focus:ring-blue-500'}),
            'status': forms.Select(attrs={'class': 'form-select block w-full rounded border-gray-300 focus:border-blue-500 focus:ring-blue-500'}),
            'due_date': forms.DateInput(attrs={'class': 'form-input block w-full rounded border-gray-300 focus:border-blue-500 focus:ring-blue-500', 'type': 'date'}),
            'priority': forms.Select(attrs={'class': 'form-select block w-full rounded border-gray-300 focus:border-blue-500 focus:ring-blue-500'}),
        }

class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-textarea block w-full rounded border-gray-300 focus:border-blue-500 focus:ring-blue-500', 'rows': 4, 'placeholder': 'Write your comment here...'}),
        } 