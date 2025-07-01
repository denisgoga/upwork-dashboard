from django.core.management.base import BaseCommand
from dashboard.upwork_service import fetch_upwork_projects

class Command(BaseCommand):
    help = 'Import projects from Upwork API'
 
    def handle(self, *args, **kwargs):
        result = fetch_upwork_projects()
        self.stdout.write(self.style.SUCCESS(f'Upwork import result: {result}')) 