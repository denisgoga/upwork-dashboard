from django.core.management.base import BaseCommand
from dashboard.models import CustomUser, Project, Task

class Command(BaseCommand):
    help = 'Seed initial data for users, projects, and tasks'

    def handle(self, *args, **kwargs):
        # Krijo përdoruesit sipas kërkesës
        devs = [
            ("Helsid Cekrezi", "Developer"),
            ("Ilda Samarxhiu", "Developer"),
            ("Denis Goga", "Developer"),
            ("Mirjan Syla", "Developer"),
            ("Eleana", "Developer"),
            ("Xhulio", "Developer"),
        ]
        for full_name, role in devs:
            first_name = full_name.split()[0]
            username = first_name.lower()
            password = first_name.capitalize() + "123"
            user, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'role': 'developer',
                    'is_superuser': False,
                    'is_staff': False,
                    'email': f'{username}@example.com',
                    'first_name': first_name,
                    'last_name': ' '.join(full_name.split()[1:]),
                }
            )
            user.set_password(password)
            user.save()

        # Admin
        admin, _ = CustomUser.objects.get_or_create(username='betaplan', defaults={
            'role': 'admin', 'is_superuser': True, 'is_staff': True, 'email': 'betaplan@example.com', 'first_name': 'BetaPlan'})
        admin.set_password('BetaPlan123')
        admin.save()

        # Merr dy developer-at e parë për të caktuar detyrat
        dev_users = list(CustomUser.objects.filter(role='developer'))
        dev1 = dev_users[0] if len(dev_users) > 0 else None
        dev2 = dev_users[1] if len(dev_users) > 1 else None

        # Create projects
        project1, _ = Project.objects.get_or_create(name='Upwork Integration', defaults={'description': 'Integrate with Upwork API'})
        project2, _ = Project.objects.get_or_create(name='Dashboard UI', defaults={'description': 'Build dashboard user interface'})

        # Create tasks
        if dev1:
            Task.objects.get_or_create(
                project=project1, title='Fetch Upwork Data', defaults={
                    'description': 'Implement Upwork API fetch', 'assignee': dev1, 'status': 'todo', 'priority': 'high'})
        if dev2:
            Task.objects.get_or_create(
                project=project1, title='Parse Upwork Response', defaults={
                    'description': 'Parse and save Upwork data', 'assignee': dev2, 'status': 'in_progress', 'priority': 'medium'})
        if dev1:
            Task.objects.get_or_create(
                project=project2, title='Create Project List UI', defaults={
                    'description': 'Show all projects in dashboard', 'assignee': dev1, 'status': 'done', 'priority': 'low'})
        if dev2:
            Task.objects.get_or_create(
                project=project2, title='Task Edit Form', defaults={
                    'description': 'Allow editing tasks', 'assignee': dev2, 'status': 'todo', 'priority': 'medium'})

        # Projekte dhe detyra të reja
        project3, _ = Project.objects.get_or_create(name='Website Redesign', defaults={'description': 'Redesign the company website'})
        project4, _ = Project.objects.get_or_create(name='Mobile App', defaults={'description': 'Develop a new mobile application'})
        project5, _ = Project.objects.get_or_create(name='API Refactor', defaults={'description': 'Refactor the backend API for performance'})

        # Merr të gjithë developer-at
        all_devs = list(CustomUser.objects.filter(role='developer'))
        if len(all_devs) >= 6:
            Task.objects.get_or_create(
                project=project3, title='Landing Page UI', defaults={
                    'description': 'Design new landing page', 'assignee': all_devs[2], 'status': 'todo', 'priority': 'high'})
            Task.objects.get_or_create(
                project=project3, title='Content Update', defaults={
                    'description': 'Update all website content', 'assignee': all_devs[3], 'status': 'in_progress', 'priority': 'medium'})
            Task.objects.get_or_create(
                project=project4, title='User Authentication', defaults={
                    'description': 'Implement login/signup in app', 'assignee': all_devs[4], 'status': 'todo', 'priority': 'high'})
            Task.objects.get_or_create(
                project=project4, title='Push Notifications', defaults={
                    'description': 'Add push notification support', 'assignee': all_devs[5], 'status': 'todo', 'priority': 'medium'})
            Task.objects.get_or_create(
                project=project5, title='Optimize Endpoints', defaults={
                    'description': 'Improve API endpoint performance', 'assignee': all_devs[0], 'status': 'todo', 'priority': 'high'})
            Task.objects.get_or_create(
                project=project5, title='Add API Docs', defaults={
                    'description': 'Document all API endpoints', 'assignee': all_devs[1], 'status': 'in_progress', 'priority': 'low'})

        self.stdout.write(self.style.SUCCESS('Seed data created successfully!')) 