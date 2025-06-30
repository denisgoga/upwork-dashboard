from django.contrib import admin
from .models import Project, Task, TaskComment, SyncLog, CustomUser

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assignee', 'status', 'priority', 'due_date')
    list_filter = ('status', 'assignee', 'project', 'priority')
    search_fields = ('title', 'description')

admin.site.register(Project)
admin.site.register(TaskComment)
admin.site.register(SyncLog)
admin.site.register(CustomUser)
