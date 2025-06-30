from django.core.management.base import BaseCommand
from dashboard.models import CustomUser, Project, Task

class Command(BaseCommand):
    help = 'Seed initial data for users, projects, and tasks'

    def handle(self, *args, **kwargs):
        # Create users
        admin, _ = CustomUser.objects.get_or_create(username='admin', defaults={
            'role': 'admin', 'is_superuser': True, 'is_staff': True, 'email': 'admin@example.com'})
        admin.set_password('admin123')
        admin.save()
        dev1, _ = CustomUser.objects.get_or_create(username='dev1', defaults={
            'role': 'developer', 'is_superuser': False, 'is_staff': False, 'email': 'dev1@example.com'})
        dev1.set_password('dev123')
        dev1.save()
        dev2, _ = CustomUser.objects.get_or_create(username='dev2', defaults={
            'role': 'developer', 'is_superuser': False, 'is_staff': False, 'email': 'dev2@example.com'})
        dev2.set_password('dev123')
        dev2.save()

        # Create projects
        project1, _ = Project.objects.get_or_create(name='Upwork Integration', defaults={'description': 'Integrate with Upwork API'})
        project2, _ = Project.objects.get_or_create(name='Dashboard UI', defaults={'description': 'Build dashboard user interface'})

        # Create tasks
        Task.objects.get_or_create(
            project=project1, title='Fetch Upwork Data', defaults={
                'description': 'Implement Upwork API fetch', 'assignee': dev1, 'status': 'todo', 'priority': 'high'})
        Task.objects.get_or_create(
            project=project1, title='Parse Upwork Response', defaults={
                'description': 'Parse and save Upwork data', 'assignee': dev2, 'status': 'in_progress', 'priority': 'medium'})
        Task.objects.get_or_create(
            project=project2, title='Create Project List UI', defaults={
                'description': 'Show all projects in dashboard', 'assignee': dev1, 'status': 'done', 'priority': 'low'})
        Task.objects.get_or_create(
            project=project2, title='Task Edit Form', defaults={
                'description': 'Allow editing tasks', 'assignee': dev2, 'status': 'todo', 'priority': 'medium'})

        self.stdout.write(self.style.SUCCESS('Seed data created successfully!')) 