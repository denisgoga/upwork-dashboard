from django.contrib import admin
from .models import Project, Task, TaskComment, SyncLog, CustomUser


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assignee', 'status', 'priority', 'due_date')
    list_filter = ('status', 'assignee', 'project', 'priority')
    search_fields = ('title', 'description')

@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'comment', 'user', 'created_at')
    list_filter = ('task', 'user')
    search_fields = ('task__title', 'user__username', 'comment')



admin.site.register(Project)
# admin.site.register()
admin.site.register(SyncLog)
admin.site.register(CustomUser)
